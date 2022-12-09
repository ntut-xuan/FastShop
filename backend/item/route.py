from __future__ import annotations

from flask import Blueprint

from util import route_with_doc

item_bp = Blueprint("item", __name__)


@route_with_doc(item_bp, "/items", methods=["GET"])
def fetch_all_items():
    pass  # pragma: no cover


@route_with_doc(item_bp, "/items", methods=["POST"])
def add_item():
    pass  # pragma: no cover


@route_with_doc(item_bp, "/items/<string:id>", methods=["GET"])
def fetch_specific_item(id):
    pass  # pragma: no cover


@route_with_doc(item_bp, "/items/<string:id>", methods=["PUT"])
def update_specific_item(id):
    pass  # pragma: no cover


@route_with_doc(item_bp, "/items/<string:id>", methods=["DELETE"])
def delete_specific_item(id):
    pass  # pragma: no cover


@route_with_doc(item_bp, "/items/<string:id>/count", methods=["GET"])
def fetch_count_of_specific_item(id):
    pass  # pragma: no cover
