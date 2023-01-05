from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask import Blueprint, current_app, make_response, request

from auth.util import HS256JWTCodec
from database import db
from models import DeliveryStatus, OrderStatus, Order, User
from util import route_with_doc

if TYPE_CHECKING:
    from flask import Response

order_bp = Blueprint("order", __name__)


@route_with_doc(order_bp, "/orders", methods=["POST"])
def create_order_from_user_shopping_cart() -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)
    jwt_token: str = request.cookies["jwt"]
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt_token)
    id_of_current_user: int | None = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).scalar_one_or_none()
    fields: dict[str, Any] = flatten_order_payload(payload) | {
        "user_id": id_of_current_user,
        "order_status": OrderStatus.CHECKING,
        "delivery_status": DeliveryStatus.PENDING,
    }
    new_order = Order(**fields)
    db.session.add(new_order)
    db.session.flush()
    payload = {"id": new_order.order_id}
    db.session.commit()
    return make_response(payload)


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
