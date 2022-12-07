from __future__ import annotations

from flasgger import swag_from
from flask import Blueprint

tag_bp = Blueprint("tag", __name__)


@tag_bp.route("/tags", methods=["GET"])
@swag_from("../api/tag/get.yml")
def fetch_all_tags():
    pass  # pragma: no cover


@tag_bp.route("/tags", methods=["POST"])
@swag_from("../api/tag/post.yml")
def add_tag():
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>", methods=["GET"])
@swag_from("../api/tag/id_get.yml")
def fetch_tag(id):
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>", methods=["PUT"])
@swag_from("../api/tag/id_put.yml")
def update_tag(id):
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>", methods=["DELETE"])
@swag_from("../api/tag/id_delete.yml")
def delete_tag(id):
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>/items", methods=["GET"])
@swag_from("../api/tag/id_items_get.yml")
def get_items_by_tag(id):
    pass  # pragma: no cover
