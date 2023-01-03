from flask import Blueprint

from util import route_with_doc

order_bp = Blueprint("order", __name__)


@route_with_doc(order_bp, "/orders", methods=["POST"])
def create_order_from_user_shopping_cart():
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders", methods=["GET"])
def fetch_all_the_order():
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["DELETE"])
def delete_order(id: int):
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["GET"])
def fetch_the_order_with_specific_id(id: int):
    pass  # pragma: no cover
