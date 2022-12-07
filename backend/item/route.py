from __future__ import annotations

from flasgger import swag_from
from flask import Blueprint

item_bp = Blueprint("item", __name__)


@item_bp.route("/items", methods=["GET"])
@swag_from("../api/item/get.yml")
def fetch_all_items():
    pass  # pragma: no cover


@item_bp.route("/items", methods=["POST"])
@swag_from("../api/item/post.yml")
def add_item():
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>", methods=["GET"])
@swag_from("../api/item/id_get.yml")
def fetch_specific_item(id):
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>", methods=["PUT"])
@swag_from("../api/item/id_put.yml")
def update_specific_item(id):
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>", methods=["DELETE"])
@swag_from("../api/item/id_delete.yml")
def delete_specific_item(id):
    pass  # pragma: no cover


@item_bp.route("/items/<string:id>/count", methods=["GET"])
@swag_from("../api/item/id_count_get.yml")
def fetch_count_of_specific_item(id):
    pass  # pragma: no cover
