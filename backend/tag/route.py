from __future__ import annotations

from http import HTTPStatus
from typing import Any, TYPE_CHECKING

from flask import Blueprint, make_response, request

from auth.util import verify_login_or_return_401
from database import db
from models import Tag
from response_message import INVALID_DATA, WRONG_DATA_FORMAT
from util import make_single_message_response, route_with_doc

if TYPE_CHECKING:
    from flask import Response
    from sqlalchemy.sql.expression import Select

tag_bp = Blueprint("tag", __name__)


@route_with_doc(tag_bp, "/tags", methods=["GET"])
def fetch_all_tags() -> Response:
    tags: list[Tag] = db.session.execute(db.select(Tag)).scalars().all()

    payload: dict[str, Any] = {
        "count": len(tags),
        "tags": [filter_sqlalchemy_meta_key(tag) for tag in tags],
    }
    return make_response(payload)


@route_with_doc(tag_bp, "/tags", methods=["POST"])
@verify_login_or_return_401
def add_tag() -> Response:
    payload: dict[str, Any] | None = request.get_json(silent=True)

    if payload is None or "name" not in payload:
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    if not type(payload["name"]) is str:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, INVALID_DATA
        )

    tag_name: str = payload["name"]

    if has_tag(tag_name):
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The tag already exists in the database."
        )

    db.session.execute(db.insert(Tag).values(name=tag_name))
    db.session.commit()
    return make_single_message_response(HTTPStatus.OK)


def has_tag(name: str) -> bool:
    select_tag_with_name_stmt: Select = db.select(Tag).where(Tag.name == name)
    tags: list[Tag] = db.session.execute(select_tag_with_name_stmt).scalars().all()
    return len(tags) != 0


@route_with_doc(tag_bp, "/tags/<int:id>", methods=["GET"])
def fetch_tag(id: int) -> Response:
    tag: Tag | None = db.session.get(Tag, id)  # type: ignore[attr-defined]

    if tag is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific ID of tag is absent."
        )

    payload: dict = filter_sqlalchemy_meta_key(tag)
    return make_response(payload)


@route_with_doc(tag_bp, "/tags/<int:id>", methods=["PUT"])
@verify_login_or_return_401
def update_tag(id: int) -> Response:
    tag: Tag | None = db.session.get(Tag, id)  # type: ignore[attr-defined]

    if tag is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific ID of tag is absent."
        )

    payload: dict[str, Any] | None = request.get_json(silent=True)

    if payload is None or "name" not in payload:
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    if not type(payload["name"]) is str:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY, INVALID_DATA
        )

    tag_name: str = payload["name"]

    db.session.execute(db.update(Tag).where(Tag.id == id).values(name=tag_name))
    db.session.commit()
    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(tag_bp, "/tags/<int:id>", methods=["DELETE"])
@verify_login_or_return_401
def delete_tag(id: int) -> Response:
    tag: Tag | None = db.session.get(Tag, id)  # type: ignore[attr-defined]

    if tag is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific ID of tag is absent."
        )

    db.session.delete(tag)
    db.session.commit()
    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(tag_bp, "/tags/<string:id>/items", methods=["GET"])
def get_items_by_tag(id):
    pass  # pragma: no cover


def filter_sqlalchemy_meta_key(tag: Tag) -> dict:
    """Returns `tag.__dict__` while filtering the metadata, which have leading underscore,
    e.g., `_sa_instance_state`.
    """
    return {k: getattr(tag, k) for k in tag.__dict__ if not k.startswith("_")}
