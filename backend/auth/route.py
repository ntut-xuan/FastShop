from __future__ import annotations

from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Iterable, Mapping, cast

from flask import Blueprint, make_response, request

from auth.exception import EmailAlreadyRegisteredError, IncorrectEmailOrPasswordError
from auth.util import (
    BIRTHDAY_FORMAT,
    JWTCodec,
    UserProfile,
    fetch_user_profile,
    is_valid_birthday,
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

        try:
            login(data["e-mail"], data["password"])
        except IncorrectEmailOrPasswordError:
            return _make_single_message_response(HTTPStatus.FORBIDDEN)
        else:
            response: Response = _make_single_message_response(HTTPStatus.OK)

            del data["password"]
            data |= fetch_user_profile(data["e-mail"])
            _set_jwt_cookie_to_response(data, response)

            return response

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
    return is_valid_birthday(data["birthday"]) and is_valid_email(data["e-mail"])


def _make_single_message_response(code: int, message: str | None = None) -> Response:
    status = SingleMessageStatus(code, message)
    return make_response(status.message, status.code)


def _set_jwt_cookie_to_response(
    payload: dict[str, Any],
    response: Response,
    expiration_time_delta: timedelta = timedelta(days=1),
) -> None:
    codec = JWTCodec()
    token: str = codec.encode(payload, expiration_time_delta)
    response.set_cookie(
        "jwt",
        value=token,
        expires=datetime.now(tz=timezone.utc) + expiration_time_delta,
    )
