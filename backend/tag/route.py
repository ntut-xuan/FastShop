from __future__ import annotations

from flask import Blueprint

from util import route_with_doc

tag_bp = Blueprint("tag", __name__)


@route_with_doc(tag_bp, "/tags", methods=["GET"])
def fetch_all_tags():
    pass  # pragma: no cover


@route_with_doc(tag_bp, "/tags", methods=["POST"])
def add_tag():
    pass  # pragma: no cover


@route_with_doc(tag_bp, "/tags/<string:id>", methods=["GET"])
def fetch_tag(id):
    pass  # pragma: no cover


@route_with_doc(tag_bp, "/tags/<string:id>", methods=["PUT"])
def update_tag(id):
    pass  # pragma: no cover


@route_with_doc(tag_bp, "/tags/<string:id>", methods=["DELETE"])
def delete_tag(id):
    pass  # pragma: no cover


@route_with_doc(tag_bp, "/tags/<string:id>/items", methods=["GET"])
def get_items_by_tag(id):
    pass  # pragma: no cover
