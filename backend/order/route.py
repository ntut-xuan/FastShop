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
def delete_order():
    pass  # pragma: no cover


@route_with_doc(order_bp, "/orders/<int:id>", methods=["GET"])
def fetch_the_order_with_specicfic_id():
    pass  # pragma: no cover
