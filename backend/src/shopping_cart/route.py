from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from flask import Blueprint, make_response, request

from src.auth.util import (
    verify_login_or_redirect_login_page,
    verify_login_or_return_401,
)
from src.database import db
from src.models import Item, ShoppingCart
from src.shopping_cart.util import fetch_user_id_from_jwt_token
from src.shopping_cart.validator import (
    validate_count_should_positive_or_return_unprocessable_entity,
    validate_data_type_or_return_unprocessable_entity,
    validate_format_or_return_bad_request,
    validate_item_exists_in_user_cart_or_return_forbidden,
    validate_item_exists_or_return_forbidden,
    validate_item_not_exists_in_user_cart_or_return_forbidden,
)
from util import make_single_message_response, route_with_doc, fetch_page

if TYPE_CHECKING:
    from sqlalchemy.engine.row import Row

shopping_cart_bp = Blueprint("shopping_cart", __name__)


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
@verify_login_or_return_401
@validate_format_or_return_bad_request
@validate_data_type_or_return_unprocessable_entity
@validate_count_should_positive_or_return_unprocessable_entity
@validate_item_exists_or_return_forbidden
@validate_item_not_exists_in_user_cart_or_return_forbidden
def add_one_item_to_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)
    payload: dict[str, Any] | None = request.get_json(silent=True)

    shopping_cart = ShoppingCart(
        user_id=user_id, count=payload["count"], item_id=payload["id"]
    )
    db.session.add(shopping_cart)
    db.session.commit()

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(shopping_cart_bp, "/shopping_cart/item", methods=["PUT"])
@verify_login_or_return_401
@validate_format_or_return_bad_request
@validate_data_type_or_return_unprocessable_entity
@validate_count_should_positive_or_return_unprocessable_entity
@validate_item_exists_or_return_forbidden
@validate_item_exists_in_user_cart_or_return_forbidden
def update_one_item_to_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)
    payload: dict[str, Any] | None = request.get_json(silent=True)

    if payload["count"] > 0:
        shopping_cart: ShoppingCart = ShoppingCart.query.filter_by(
            user_id=user_id, item_id=payload["id"]
        ).first()
        shopping_cart.count = payload["count"]
        db.session.commit()
    else:
        db.session.execute(
            db.delete(ShoppingCart).where(
                ShoppingCart.user_id == user_id, ShoppingCart.item_id == payload["id"]
            )
        )
        db.session.commit()

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(shopping_cart_bp, "/shopping_cart", methods=["DELETE"])
@verify_login_or_return_401
def delete_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)

    db.session.execute(db.delete(ShoppingCart).where(ShoppingCart.user_id == user_id))
    db.session.commit()

    return make_single_message_response(HTTPStatus.OK)


@shopping_cart_bp.route("/cart", methods=["GET"])
@verify_login_or_redirect_login_page
def shopping_cart_page_route() -> str:
    return fetch_page("shopping_cart")
