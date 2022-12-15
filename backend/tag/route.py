from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flask import Blueprint, make_response

from database import db
from models import Tag
from util import route_with_doc

if TYPE_CHECKING:
    from flask import Response

tag_bp = Blueprint("tag", __name__)


@route_with_doc(tag_bp, "/tags", methods=["GET"])
def fetch_all_tags() -> Response:
    tags: list[Tag] = db.session.execute(db.select(Tag)).scalars().all()

    payload: dict[str, Any] = {
        "count": len(tags),
        "tags": [filter_sqlalchemy_meta_key(tag) for tag in tags],
    }
    return make_response(payload)


def filter_sqlalchemy_meta_key(tag: Tag) -> dict:
    """Returns `tag.__dict__` while filtering the metadata, which have leading underscore,
    e.g., `_sa_instance_state`.
    """
    return {k: getattr(tag, k) for k in tag.__dict__ if not k.startswith("_")}


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
