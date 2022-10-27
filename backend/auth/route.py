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
from util import SingleMessageStatus, fetch_page

if TYPE_CHECKING:
    from flask.wrappers import Response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route() -> Response | str:
    if request.method == "POST":
        data = request.json

        if data is None or "e-mail" not in data or "password" not in data:
            return _make_single_message_response(HTTPStatus.BAD_REQUEST)
        if not is_valid_email(data["e-mail"]):
            return _make_single_message_response(HTTPStatus.UNPROCESSABLE_ENTITY)

        status_code: HTTPStatus
        if not login(data["e-mail"], data["password"]):
            status_code = HTTPStatus.FORBIDDEN
        else:
            status_code = HTTPStatus.OK
        return _make_single_message_response(status_code)

    return fetch_page("login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_route() -> Response | str:
    if request.method == "POST":
        # 400 Bad Request error will automatically be raised
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
        if not all([col in data for col in required_columns]):
            return _make_single_message_response(HTTPStatus.BAD_REQUEST)
        if not is_valid_birthday_format(data["birthday"]):
            return _make_single_message_response(HTTPStatus.UNPROCESSABLE_ENTITY)
        if not is_valid_email(data["e-mail"]):
            return _make_single_message_response(HTTPStatus.UNPROCESSABLE_ENTITY)

        profile = UserProfile(
            firstname=data["firstname"],
            lastname=data["lastname"],
            sex=data["sex"],
            birthday=int(
                datetime.strptime(data["birthday"], BIRTHDAY_FORMAT).timestamp()
            ),
        )
        status_code: HTTPStatus
        if not register(data["e-mail"], data["password"], profile):
            status_code = HTTPStatus.FORBIDDEN
        else:
            status_code = HTTPStatus.OK
        return _make_single_message_response(status_code)

    return fetch_page("register")


def _make_single_message_response(code: int, message: str | None = None) -> Response:
    status = SingleMessageStatus(code, message)
    return make_response(status.message, status.code)
