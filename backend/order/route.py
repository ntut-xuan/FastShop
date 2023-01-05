from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from flask import Blueprint, current_app, make_response, request

from auth.util import HS256JWTCodec, verify_login_or_return_401
from database import db
from order.util import (
    add_items_of_order,
    add_order_of_user,
    has_non_existent_item,
    has_unavailable_count_of_item,
    flatten_order_payload,
)
from models import DeliveryStatus, OrderStatus, User
from util import make_single_message_response, route_with_doc

if TYPE_CHECKING:
    from flask import Response

order_bp = Blueprint("order", __name__)


@route_with_doc(order_bp, "/orders", methods=["POST"])
@verify_login_or_return_401
def create_order_from_user_shopping_cart() -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)
    assert payload is not None  # TODO: handle missing payload
    id_of_current_user: int | None = get_uid_from_jwt(request.cookies["jwt"])
    assert (
        id_of_current_user is not None
    )  # `verify_login_or_return_401` has validated the user

    item_ids_and_counts: list[dict[str, Any]] = payload["items"]
    if has_non_existent_item(item_ids_and_counts) or has_unavailable_count_of_item(
        item_ids_and_counts
    ):
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "Exists unavailable item in the order."
        )

    fields_and_values: dict[str, Any] = flatten_order_payload(payload) | {
        # default values of statuses
        "order_status": OrderStatus.CHECKING,
        "delivery_status": DeliveryStatus.PENDING,
    }
    order_id: int = add_order_of_user(id_of_current_user, fields_and_values)
    add_items_of_order(order_id, item_ids_and_counts)

    response: Response = make_response({"id": order_id})
    return response


def get_uid_from_jwt(jwt: str) -> int | None:
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt)
    uid: int | None = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).scalar_one_or_none()
    return uid


@route_with_doc(order_bp, "/orders", methods=["GET"])
def fetch_all_the_order():
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["DELETE"])
def delete_order(id: int):
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["GET"])
def fetch_the_order_with_specific_id(id: int):
    pass  # pragma: no cover
