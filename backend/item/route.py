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
