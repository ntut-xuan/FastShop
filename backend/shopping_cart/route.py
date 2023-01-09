from typing import TYPE_CHECKING, Any, cast

from http import HTTPStatus
from flask import Blueprint, current_app, make_response, request

from auth.util import HS256JWTCodec, verify_login_or_return_401
from database import db
from flask import Response
from models import Item, ShoppingCart, User
from pydantic import BaseModel, StrictInt
from pydantic.dataclasses import dataclass
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError
from util import route_with_doc, make_single_message_response
from response_message import INVALID_DATA, WRONG_DATA_FORMAT

if TYPE_CHECKING:
    from sqlalchemy.engine.row import Row

shopping_cart_bp = Blueprint("shopping_cart", __name__)


class ItemNotExistError(ValueError):
    pass


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
@verify_login_or_return_401
def add_one_item_to_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)
    payload: dict[str, Any] | None = request.get_json(silent=True)

    validate_response: Response = _validate_shopping_cart_payload(payload)
    if validate_response.status_code != HTTPStatus.OK:
        return validate_response

    try:
        db.session.execute(
            db.insert(ShoppingCart),
            [{"user_id": user_id, "count": payload["count"], "item_id": payload["id"]}],
        )
    except IntegrityError:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The item already exists in cart."
        )

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(shopping_cart_bp, "/shopping_cart/item", methods=["PUT"])
@verify_login_or_return_401
def update_one_item_to_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)
    payload: dict[str, Any] | None = request.get_json(silent=True)

    validate_response: Response = _validate_shopping_cart_payload(payload)
    if validate_response.status_code != HTTPStatus.OK:
        return validate_response

    shopping_cart: ShoppingCart | None = ShoppingCart.query.filter_by(
        user_id=user_id, item_id=payload["id"]
    ).first()
    if shopping_cart == None:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, "The ID of the payload is absent in items."
        )

    shopping_cart.count = payload["count"]
    db.session.commit()

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(shopping_cart_bp, "/shopping_cart", methods=["DELETE"])
@verify_login_or_return_401
def delete_the_shopping_cart():
    jwt_token: str = request.cookies.get("jwt")
    user_id: int = fetch_user_id_from_jwt_token(jwt_token)

    db.session.execute(db.delete(ShoppingCart).where(ShoppingCart.user_id == user_id))

    return make_single_message_response(HTTPStatus.OK)


def _validate_shopping_cart_payload(payload: dict[str, Any]):
    """
    Validate the payload with validator, except won't raise any error if payload is valid.
    """

    @dataclass
    class Validator:
        count: StrictInt
        id: StrictInt

    def validate_count(count):
        if count < 0:
            raise ValueError("Count should be positive.")

    def validate_item_is_exists(item_id):
        item: Item | None = Item.query.filter_by(id=item_id).first()
        if item == None:
            raise ItemNotExistError("Item with specific ID is not exists.")

    try:
        Validator(**payload)
        validate_count(payload["count"])
        validate_item_is_exists(payload["id"])
    except ItemNotExistError as error:
        return make_single_message_response(HTTPStatus.FORBIDDEN, str(error))
    except ValueError:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, INVALID_DATA
        )
    except TypeError:
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    return make_single_message_response(HTTPStatus.OK)
