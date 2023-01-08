from typing import TYPE_CHECKING, Any, cast

from flask import Blueprint, current_app, make_response, request

from auth.util import HS256JWTCodec, verify_login_or_return_401
from database import db
from models import Item, ShoppingCart, User
from util import route_with_doc

if TYPE_CHECKING:
    from sqlalchemy.engine.row import Row

shopping_cart_bp = Blueprint("shopping_cart", __name__)


def fetch_user_id_from_jwt_token(jwt_token: str) -> int:
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt_token)
    user: User = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).fetchone()
    return cast(int, user.uid)


@route_with_doc(shopping_cart_bp, "/shopping_cart", methods=["GET"])
@verify_login_or_return_401
def get_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)

    # Item detail should have ID, count and discount.
    user_cart_item_details: list[Row] = db.session.execute(
        db.select(ShoppingCart.item_id, ShoppingCart.count, Item.discount)
        .select_from(ShoppingCart)
        .join(Item)
        .where(ShoppingCart.user_id == user_id)
    ).all()

    items: list[dict[str, Any]] = []
    items_total_price = 0

    for item_details in user_cart_item_details:
        items.append(
            {
                "count": item_details.count,
                "id": item_details.item_id,
                "price": item_details.discount,
            }
        )
        items_total_price += item_details.discount * item_details.count

    result = {"count": len(items), "items": items, "price": items_total_price}
    return make_response(result)


@route_with_doc(shopping_cart_bp, "/shopping_cart/item", methods=["POST"])
def add_one_item_to_the_shopping_cart():
    pass  # pragma: no cover.


@route_with_doc(shopping_cart_bp, "/shopping_cart/item", methods=["PUT"])
def update_one_item_to_the_shopping_cart():
    pass  # pragma: no cover.


@route_with_doc(shopping_cart_bp, "/shopping_cart", methods=["DELETE"])
def delete_the_shopping_cart():
    pass  # pragma: no cover.
