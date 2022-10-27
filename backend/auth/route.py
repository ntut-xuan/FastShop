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

        if data is None or "e-mail" not in data or "password" not in data:
            return make_response((Status.INVALID_DATA.value, HTTPStatus.BAD_REQUEST))

        email = data["e-mail"]
        password = data["password"]

        if not is_valid_email(email):
            return make_response(
                (Status.INVALID_EMAIL.value, HTTPStatus.UNPROCESSABLE_ENTITY)
            )

        if not login(email, password):
            return make_response((Status.INCORRECT_LOGIN.value, HTTPStatus.FORBIDDEN))

        return make_response((Status.OK.value, HTTPStatus.OK))

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
        # Check column is exist in json data
        if not all([col in data for col in required_columns]):
            return make_response((Status.INVALID_DATA.value, HTTPStatus.BAD_REQUEST))

        # Validate the data
        if not is_valid_birthday_format(data["birthday"]):
            return make_response(
                (Status.INVALID_DATA.value, HTTPStatus.UNPROCESSABLE_ENTITY)
            )

        if not is_valid_email(data["e-mail"]):
            return make_response(
                (Status.INVALID_EMAIL.value, HTTPStatus.UNPROCESSABLE_ENTITY)
            )

        profile = UserProfile(
            firstname=data["firstname"],
            lastname=data["lastname"],
            sex=data["sex"],
            birthday=int(
                datetime.strptime(data["birthday"], BIRTHDAY_FORMAT).timestamp()
            ),
        )

        # Register data
        if not register(data["e-mail"], data["password"], profile):
            return make_response((Status.INCORRECT_LOGIN.value, HTTPStatus.FORBIDDEN))

        return make_response((Status.OK.value, HTTPStatus.OK))

    return fetch_page("register")
