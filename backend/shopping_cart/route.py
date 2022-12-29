from flask import Blueprint

from util import route_with_doc

shopping_cart_bp = Blueprint("shopping_cart", __name__)


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
