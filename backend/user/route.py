from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from flask import Blueprint, current_app, make_response, request

from auth.util import BIRTHDAY_FORMAT, HS256JWTCodec, verify_login_or_return_401

if TYPE_CHECKING:
    from flask import Response

user_bp = Blueprint("user", __name__)


@user_bp.route("/user", methods=["GET"])
@verify_login_or_return_401
def fetch_profile_of_current_user() -> Response:
    # `verify_login_or_return_401` has validated the jwt cookie
    jwt_token: str = request.cookies["jwt"]
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])

    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt_token)
    user_profile: dict[str, Any] = jwt_payload["data"]
    user_profile["birthday"] = time.strftime(
        BIRTHDAY_FORMAT, time.gmtime(user_profile["birthday"])
    )
    return make_response(user_profile)
