from typing import Any, cast

from flask import current_app

from src.auth.util import HS256JWTCodec
from src.database import db
from src.models import User


def fetch_user_id_from_jwt_token(jwt_token: str) -> int:
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt_token)
    user: User = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).fetchone()
    return cast(int, user.uid)
