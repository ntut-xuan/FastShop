from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask import Blueprint, current_app, make_response, request

from auth.util import HS256JWTCodec
from database import db
from models import DeliveryStatus, ItemOfOrder, Order, OrderStatus, User
from util import route_with_doc

if TYPE_CHECKING:
    from flask import Response

order_bp = Blueprint("order", __name__)


@route_with_doc(order_bp, "/orders", methods=["POST"])
def create_order_from_user_shopping_cart() -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)
    jwt: str = request.cookies["jwt"]
    id_of_current_user: int | None = get_uid_from_jwt(jwt)

    fields_and_values: dict[str, Any] = flatten_order_payload(payload) | {
        "user_id": id_of_current_user,
        # default values of statuses
        "order_status": OrderStatus.CHECKING,
        "delivery_status": DeliveryStatus.PENDING,
    }
    new_order = Order(**fields_and_values)
    db.session.add(new_order)
    db.session.flush()

    add_items_of_order(new_order.order_id, item_ids_and_counts=payload["items"])

    response: Response = make_response({"id": new_order.order_id})
    db.session.commit()
    return response


def add_items_of_order(
    order_id: int, item_ids_and_counts: list[dict[str, int]]
) -> None:
    for item_id_and_count in item_ids_and_counts:
        db.session.add(
            ItemOfOrder(
                order_id=order_id,
                item_id=item_id_and_count["id"],
                count=item_id_and_count["count"],
            )
        )
    db.session.commit()


def get_uid_from_jwt(jwt: str) -> int | None:
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt)
    uid: int | None = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).scalar_one_or_none()
    return uid


def flatten_order_payload(payload: dict[str, Any]) -> dict[str, Any]:
    flat_payload: dict[str, Any] = {
        "date": payload["date"],
        "note": payload["note"],
        "delivery_email": payload["delivery_info"]["email"],
        "delivery_firstname": payload["delivery_info"]["firstname"],
        "delivery_lastname": payload["delivery_info"]["lastname"],
        "delivery_address": payload["delivery_info"]["address"],
        "phone": payload["delivery_info"]["phone_number"],
    }
    return flat_payload


@route_with_doc(order_bp, "/orders", methods=["GET"])
def fetch_all_the_order():
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["DELETE"])
def delete_order(id: int):
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["GET"])
def fetch_the_order_with_specific_id(id: int):
    pass  # pragma: no cover
