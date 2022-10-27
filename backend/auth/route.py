from __future__ import annotations

from datetime import datetime
from http import HTTPStatus
from typing import TYPE_CHECKING, cast

from flask import Blueprint, make_response, request

from auth.util import (
    BIRTHDAY_FORMAT,
    UserProfile,
    is_valid_birthday_format,
    is_valid_email,
    login,
    register,
)
from util import Status, fetch_page

if TYPE_CHECKING:
    from flask.wrappers import Response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route() -> Response | str:
    if request.method == "POST":
        data = request.json

        status: Status
        status_code: HTTPStatus
        if data is None or "e-mail" not in data or "password" not in data:
            status = Status.INVALID_DATA
            status_code = HTTPStatus.BAD_REQUEST
        elif not is_valid_email(data["e-mail"]):
            status = Status.INVALID_EMAIL
            status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        elif not login(data["e-mail"], data["password"]):
            status = Status.INCORRECT_LOGIN
            status_code = HTTPStatus.FORBIDDEN
        else:
            status = Status.OK
            status_code = HTTPStatus.OK
        return make_response(status.value, status_code)

    return fetch_page("login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_route() -> Response | str:
    if request.method == "POST":
        # HTTPStatus.BAD_REQUEST Bad Request error will automatically be raised
        # if the content-type is not "application/json", so
        # it's safe to cast it manually for type warning supression.
        data = cast(dict, request.json)

        required_columns: list[str] = [
            "firstname",
            "lastname",
            "sex",
            "birthday",
            "e-mail",
            "password",
        ]
        status: Status
        status_code: HTTPStatus
        if not all([col in data for col in required_columns]):
            status = Status.INVALID_DATA
            status_code = HTTPStatus.BAD_REQUEST
        elif not is_valid_birthday_format(data["birthday"]):
            status = Status.INVALID_DATA
            status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        elif not is_valid_email(data["e-mail"]):
            status = Status.INVALID_EMAIL
            status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        else:
            profile = UserProfile(
                firstname=data["firstname"],
                lastname=data["lastname"],
                sex=data["sex"],
                birthday=int(
                    datetime.strptime(data["birthday"], BIRTHDAY_FORMAT).timestamp()
                ),
            )
            if not register(data["e-mail"], data["password"], profile):
                status = Status.INCORRECT_LOGIN
                status_code = HTTPStatus.FORBIDDEN
            else:
                status = Status.OK
                status_code = HTTPStatus.OK
        return make_response(status.value, status_code)

    return fetch_page("register")
