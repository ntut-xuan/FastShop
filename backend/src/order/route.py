from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from flask import Blueprint, current_app, make_response, redirect, request
from pydantic import ValidationError

from response_message import INVALID_DATA, WRONG_DATA_FORMAT
from src.auth.util import (
    HS256JWTCodec,
    verify_login_or_redirect_login_page,
    verify_login_or_return_401,
)
from src.database import db
from src.order.util import (
    PayloadTypeChecker,
    add_items_of_order,
    add_order_of_user,
    has_non_existent_item,
    has_unavailable_count_of_item,
    flatten_order_payload,
)
from src.models import DeliveryStatus, ItemOfOrder, Order, OrderStatus, User
from util import fetch_page, make_single_message_response, route_with_doc

if TYPE_CHECKING:
    from flask import Response

order_bp = Blueprint("order", __name__)


@route_with_doc(order_bp, "/orders", methods=["POST"])
@verify_login_or_return_401
def create_order_for_current_user() -> Response:
    id_of_current_user: int | None = _get_uid_from_jwt(request.cookies["jwt"])
    # `verify_login_or_return_401` has already checked
    assert id_of_current_user is not None

    payload: dict[str, Any] | None = request.get_json(silent=True)
    if payload is None:
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    item_ids_and_counts: list[dict[str, Any]] = payload["items"]
    if has_non_existent_item(item_ids_and_counts) or has_unavailable_count_of_item(
        item_ids_and_counts
    ):
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "Exists unavailable item in the order."
        )

    default_statues: dict[str, Any] = {
        "order_status": OrderStatus.CHECKING,
        "delivery_status": DeliveryStatus.PENDING,
    }
    fields_and_values: dict[str, Any] = default_statues
    try:
        fields_and_values |= flatten_order_payload(payload)
    except KeyError:  # missing key
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    try:
        PayloadTypeChecker.Order(**fields_and_values)
    except ValidationError:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, INVALID_DATA
        )

    order_id: int = add_order_of_user(id_of_current_user, fields_and_values)
    add_items_of_order(order_id, item_ids_and_counts)
    return make_response({"id": order_id})


@route_with_doc(order_bp, "/orders", methods=["GET"])
@verify_login_or_return_401
def fetch_all_the_order() -> Response:
    uid: int | None = _get_uid_from_jwt(request.cookies["jwt"])
    # `verify_login_or_return_401` has already checked that the jwt is valid
    assert uid is not None

    orders: list[Order] = _get_orders_of_user(uid)

    payload: dict[str, Any] = {
        "count": len(orders),
        "result": [_get_response_payload_of_order(order) for order in orders],
    }
    return make_response(payload)


@route_with_doc(order_bp, "/orders/<int:id>", methods=["DELETE"])
@verify_login_or_return_401
def delete_order(id: int) -> Response:
    order: Order | None = db.session.get(Order, id)  # type: ignore[attr-defined]
    if order is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific ID of order is absent."
        )

    if order.delivery_status in {DeliveryStatus.DELIVERING, DeliveryStatus.DELIVERED}:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN,
            "The order is not possible to be deleted since the order is now delivering or has been delivered.",
        )

    db.session.delete(order)
    db.session.commit()
    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(order_bp, "/orders/<int:id>", methods=["GET"])
@verify_login_or_return_401
def fetch_the_order_with_specific_id(id: int) -> Response:
    uid: int | None = _get_uid_from_jwt(request.cookies["jwt"])
    # `verify_login_or_return_401` has already checked that the jwt is valid
    assert uid is not None

    order: Order | None = db.session.get(Order, id)  # type: ignore[attr-defined]
    if order is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific ID of the order is absent."
        )

    return make_response(_get_response_payload_of_order(order))


@order_bp.route("/order_confirmation", methods=["GET"])
@verify_login_or_redirect_login_page
def order_confrimation() -> str:
    return fetch_page("order_confirmation")


@order_bp.route("/order_detail/<int:order_id>", methods=["GET"])
@verify_login_or_redirect_login_page
def order_detail(order_id) -> str:
    uid: int | None = _get_uid_from_jwt(request.cookies["jwt"])
    assert uid is not None

    order: Order | None = Order.query.filter_by(order_id=order_id, user_id=uid).first()
    if order == None:
        return redirect("/")

    return fetch_page("order_detail")


def _get_uid_from_jwt(jwt: str) -> int | None:
    jwt_codec = HS256JWTCodec(current_app.config["jwt_key"])
    jwt_payload: dict[str, Any] = jwt_codec.decode(jwt)
    uid: int | None = db.session.execute(
        db.select(User.uid).where(User.email == jwt_payload["data"]["e-mail"])
    ).scalar_one_or_none()
    return uid


def _get_orders_of_user(user_id: int) -> list[Order]:
    orders_of_user: list[Order] = (  # temp var for type casting, otherwise it's Any
        db.session.execute(db.select(Order).where(Order.user_id == user_id))
        .scalars()
        .all()
    )
    return orders_of_user


def _get_response_payload_of_order(order: Order) -> dict[str, Any]:
    user: User | None = db.session.get(User, order.user_id)  # type: ignore[attr-defined]
    assert user is not None  # foreign key constraint should keep this True
    return {
        "id": order.order_id,
        "status": order.order_status.name,
        "delivery_status": order.delivery_status.name,
        "detail": {
            "date": order.date,
            "delivery_info": {
                "address": order.delivery_address,
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "phone_number": order.phone,
            },
            "items": _get_items_of_order(order.order_id),
            "note": order.note,
        },
    }


def _get_items_of_order(order_id: int) -> list[dict[str, int]]:
    items_of_order: list[ItemOfOrder] = (
        db.session.execute(
            db.select(ItemOfOrder).where(ItemOfOrder.order_id == order_id)
        )
        .scalars()
        .all()
    )
    return [{"id": item.item_id, "count": item.count} for item in items_of_order]
