from typing import Any, cast

from flask import Blueprint, current_app

from auth.util import HS256JWTCodec
from database import db
from models import User
from util import route_with_doc

shopping_cart_bp = Blueprint("shopping_cart", __name__)


def fetch_user_id_from_jwt_token(jwt_token: str) -> int:
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt_token)
    user: User = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).fetchone()
    return cast(int, user.uid)


@route_with_doc(shopping_cart_bp, "/shopping_cart", methods=["GET"])
def get_the_shopping_cart():
    pass  # pragma: no cover.


@route_with_doc(shopping_cart_bp, "/shopping_cart/item", methods=["POST"])
def add_one_item_to_the_shopping_cart():
    pass  # pragma: no cover.


@route_with_doc(shopping_cart_bp, "/shopping_cart/item", methods=["PUT"])
def update_one_item_to_the_shopping_cart():
    pass  # pragma: no cover.


@route_with_doc(shopping_cart_bp, "/shopping_cart", methods=["DELETE"])
def delete_the_shopping_cart():
    pass  # pragma: no cover.
