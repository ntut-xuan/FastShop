from flask import Blueprint

from util import route_with_doc

shoppingcart_bp = Blueprint("shoppingcart", __name__)


@route_with_doc(shoppingcart_bp, "/shoppingcart", methods=["GET"])
def get_the_shoppingcart():
    pass  # pragma: no cover.


@route_with_doc(shoppingcart_bp, "/shoppingcart/item", methods=["POST"])
def add_one_item_to_the_shoppingcart():
    pass  # pragma: no cover.


@route_with_doc(shoppingcart_bp, "/shoppingcart/item", methods=["PUT"])
def update_one_item_to_the_shoppingcart():
    pass  # pragma: no cover.


@route_with_doc(shoppingcart_bp, "/shoppingcart", methods=["DELETE"])
def delete_the_shoppingcart():
    pass  # pragma: no cover.
