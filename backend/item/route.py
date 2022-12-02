from __future__ import annotations

from flasgger import swag_from
from flask import Blueprint

item_bp = Blueprint("item", __name__)


@item_bp.route("/items", methods=["GET"])
@swag_from("../api/items_get.yml")
def fetch_all_items():
    pass


@item_bp.route("/items", methods=["POST"])
@swag_from("../api/items_post.yml")
def add_item():
    pass


@item_bp.route("/items/<string:ID>", methods=["GET"])
@swag_from("../api/items_specific_item_get.yml")
def fetch_specific_item(ID):
    pass


@item_bp.route("/items/<string:ID>", methods=["PUT"])
@swag_from("../api/items_specific_item_put.yml")
def update_specific_item(ID):
    pass


@item_bp.route("/items/<string:ID>", methods=["DELETE"])
@swag_from("../api/items_specific_item_delete.yml")
def delete_specific_item(ID):
    pass
