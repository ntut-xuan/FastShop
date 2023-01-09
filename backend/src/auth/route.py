from __future__ import annotations

from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Iterable, Mapping, cast

from flask import Blueprint, Response, current_app, make_response, request

from src.auth.exception import EmailAlreadyRegisteredError
from src.auth.util import (
    BIRTHDAY_FORMAT,
    HS256JWTCodec,
    UserProfile,
    fetch_user_profile,
    is_correct_password,
    is_registered,
    is_valid_birthday,
    is_valid_email,
    register,
)
from response_message import (
    ABSENT_COOKIE,
    DUPLICATE_ACCOUNT,
    INCORRECT_EMAIL_OR_PASSWORD,
    INVALID_COOKIE,
    INVALID_DATA,
    WRONG_DATA_FORMAT,
)
from util import fetch_page, make_single_message_response, route_with_doc

if TYPE_CHECKING:
    from flask.wrappers import Response

auth_bp = Blueprint("auth", __name__)


@route_with_doc(auth_bp, "/login", methods=["GET", "POST"])
def login_route() -> Response | str:
    if request.method == "POST":
        data = request.json

        if data is None or "e-mail" not in data or "password" not in data:
            return make_single_message_response(
                HTTPStatus.BAD_REQUEST, message=WRONG_DATA_FORMAT
            )
        if not is_valid_email(data["e-mail"]):
            return make_single_message_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, message=INVALID_DATA
            )

        if not _is_correct_email_and_password(data["e-mail"], data["password"]):
            return make_single_message_response(
                HTTPStatus.FORBIDDEN, message=INCORRECT_EMAIL_OR_PASSWORD
            )
        else:
            response: Response = make_single_message_response(HTTPStatus.OK)

            # Not using `del data["password"] because there might be something
            # other then e-mail and password in the posted data`.
            payload: dict[str, Any] = {"e-mail": data["e-mail"]}
            payload |= fetch_user_profile(data["e-mail"])
            _set_jwt_cookie_to_response(payload, response)

            return response

    return fetch_page("login")


@route_with_doc(auth_bp, "/register", methods=["GET", "POST"])
def register_route() -> Response | str:
    if request.method == "POST":
        # 400 Bad Request error will automatically be raised
        # if the content-type is not "application/json", so
        # it's safe to cast it manually for type warning suppression.
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
            return make_single_message_response(
                HTTPStatus.BAD_REQUEST, message=WRONG_DATA_FORMAT
            )
        if not _has_valid_register_data_format(data):
            return make_single_message_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, message=INVALID_DATA
            )

        profile = UserProfile(
            firstname=data["firstname"],
            lastname=data["lastname"],
            gender=data["gender"],
            birthday=int(
                datetime.strptime(data["birthday"], BIRTHDAY_FORMAT).timestamp()
            ),
        )
        try:
            register(data["e-mail"], data["password"], profile)
        except EmailAlreadyRegisteredError:
            return make_single_message_response(
                HTTPStatus.FORBIDDEN, message=DUPLICATE_ACCOUNT
            )
        else:
            return make_single_message_response(HTTPStatus.OK)

    return fetch_page("register")


@route_with_doc(auth_bp, "/verify_jwt", methods=["POST"])
def verify_jwt_route() -> Response:
    if "jwt" not in request.cookies:
        return make_single_message_response(HTTPStatus.UNAUTHORIZED, ABSENT_COOKIE)

    jwt_token: str = request.cookies["jwt"]
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])

    if not jwt_codec.is_valid_jwt(jwt_token):
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, INVALID_COOKIE
        )

    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt_token)
    return make_response(jwt_payload)


@route_with_doc(auth_bp, "/logout", methods=["POST"])
def logout_route() -> Response:
    response: Response = make_single_message_response(HTTPStatus.OK)
    response.delete_cookie("jwt")
    return response


def _is_correct_email_and_password(email: str, password: str) -> bool:
    return is_registered(email) and is_correct_password(email, password)


def _has_required_columns(data: Mapping, required_columns: Iterable) -> bool:
    return all([col in data for col in required_columns])


def _has_valid_register_data_format(data: Mapping[str, Any]) -> bool:
    return is_valid_birthday(data["birthday"]) and is_valid_email(data["e-mail"])


def _set_jwt_cookie_to_response(
    payload: dict[str, Any],
    response: Response,
    expiration_time_delta: timedelta = timedelta(days=1),
) -> None:
    codec = HS256JWTCodec(current_app.config["jwt_key"])
    token: str = codec.encode(payload, expiration_time_delta)
    response.set_cookie(
        "jwt",
        value=token,
        expires=datetime.now(tz=timezone.utc) + expiration_time_delta,
    )
