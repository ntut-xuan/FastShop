from __future__ import annotations

from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Iterable, Mapping, cast

from flask import Blueprint, make_response, request
from auth.exception import EmailAlreadyRegisteredError, IncorrectEmailOrPasswordError

from auth.util import (
    BIRTHDAY_FORMAT,
    UserProfile,
    fetch_specific_account_profile,
    generate_payload,
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

        if data is None or not _has_required_login_data(data):
            return _make_single_message_response(HTTPStatus.BAD_REQUEST)
        if not is_valid_email(data["e-mail"]):
            return _make_single_message_response(HTTPStatus.UNPROCESSABLE_ENTITY)

        status_code: HTTPStatus
        try:
            login(data["e-mail"], data["password"])
        except IncorrectEmailOrPasswordError:
            status_code = HTTPStatus.FORBIDDEN
        else:
            status_code = HTTPStatus.OK

        prepare_response = _make_single_message_response(status_code)

        if status_code == HTTPStatus.OK:
            del data["password"]
            data |= fetch_specific_account_profile(data["e-mail"])
            prepare_response = _set_jwt_cookie_to_response(data, prepare_response)

        return prepare_response

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
            "gender",
            "birthday",
            "e-mail",
            "password",
        ]
        if not _has_required_columns(data, required_columns):
            return _make_single_message_response(HTTPStatus.BAD_REQUEST)
        if not _has_valid_register_data_format(data):
            return _make_single_message_response(HTTPStatus.UNPROCESSABLE_ENTITY)

        profile = UserProfile(
            firstname=data["firstname"],
            lastname=data["lastname"],
            gender=data["gender"],
            birthday=int(
                datetime.strptime(data["birthday"], BIRTHDAY_FORMAT).timestamp()
            ),
        )
        status_code: HTTPStatus
        try:
            register(data["e-mail"], data["password"], profile)
        except EmailAlreadyRegisteredError:
            status_code = HTTPStatus.FORBIDDEN
        else:
            status_code = HTTPStatus.OK
        return _make_single_message_response(status_code)

    return fetch_page("register")


def _has_required_login_data(data: Mapping[str, Any]) -> bool:
    return "e-mail" in data and "password" in data


def _has_required_columns(data: Mapping, required_columns: Iterable) -> bool:
    return all([col in data for col in required_columns])


def _has_valid_register_data_format(data: Mapping[str, Any]) -> bool:
    return is_valid_birthday_format(data["birthday"]) and is_valid_email(data["e-mail"])


def _make_single_message_response(code: int, message: str | None = None) -> Response:
    status = SingleMessageStatus(code, message)
    return make_response(status.message, status.code)


def _set_jwt_cookie_to_response(data: dict, response: Response):
    current_time: datetime = datetime.now(tz=timezone.utc)
    expiration_time: datetime = current_time + timedelta(days=1)
    jwt_data: str = generate_payload(data)
    response.set_cookie("cd_wy_sbl", value=jwt_data, expires=expiration_time)
    return response
