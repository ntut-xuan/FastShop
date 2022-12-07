from __future__ import annotations

from flask import Blueprint

from util import register_swagger_file

tag_bp = Blueprint("tag", __name__)


@tag_bp.route("/tags", methods=["GET"])
@register_swagger_file("tag", "get", methods=["GET"])
def fetch_all_tags():
    pass  # pragma: no cover


@tag_bp.route("/tags", methods=["POST"])
@register_swagger_file("tag", "post", methods=["POST"])
def add_tag():
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>", methods=["GET"])
@register_swagger_file("tag", "id_get", methods=["GET"])
def fetch_tag(id):
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>", methods=["PUT"])
@register_swagger_file("tag", "id_put", methods=["PUT"])
def update_tag(id):
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>", methods=["DELETE"])
@register_swagger_file("tag", "id_delete", methods=["DELETE"])
def delete_tag(id):
    pass  # pragma: no cover


@tag_bp.route("/tags/<string:id>/items", methods=["GET"])
@register_swagger_file("tag", "id_items_get", methods=["GET"])
def get_items_by_tag(id):
    pass  # pragma: no cover
