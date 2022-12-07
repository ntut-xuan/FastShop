from __future__ import annotations

from flask import Blueprint

from util import register_swagger_file

item_bp = Blueprint("item", __name__)


@item_bp.route("/items", methods=["GET"])
@register_swagger_file("item", "get", methods=["GET"])
def fetch_all_items():
    pass  # pragma: no cover


@item_bp.route("/items", methods=["POST"])
@register_swagger_file("item", "post", methods=["POST"])
def add_item():
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>", methods=["GET"])
@register_swagger_file("item", "id_get", methods=["GET"])
def fetch_specific_item(id):
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>", methods=["PUT"])
@register_swagger_file("item", "id_put", methods=["PUT"])
def update_specific_item(id):
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>", methods=["DELETE"])
@register_swagger_file("item", "id_delete", methods=["DELETE"])
def delete_specific_item(id):
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>/count", methods=["GET"])
@register_swagger_file("item", "id_count_get", methods=["GET"])
def fetch_count_of_specific_item(id):
    pass  # pragma: no cover
