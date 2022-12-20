from __future__ import annotations

from http import HTTPStatus
from typing import Any, cast

from flask import Blueprint, make_response, request
from pydantic import ValidationError

from auth.util import verify_login_or_return_401
from database import db
from item.util import PayloadTypeChecker, flatten_item_payload
from models import Item, TagOfItem
from util import make_single_message_response, route_with_doc

item_bp = Blueprint("item", __name__)


@route_with_doc(item_bp, "/items", methods=["GET"])
def fetch_all_items():
    pass  # pragma: no cover


@route_with_doc(item_bp, "/items", methods=["POST"])
@verify_login_or_return_401
def add_item():
    payload: dict[str, Any] = cast(dict, request.json)
    try:
        flat_payload: dict[str, Any] = flatten_item_payload(payload)
        tag_ids: list[int] = payload["tags"]
    except KeyError:
        return make_single_message_response(
            HTTPStatus.BAD_REQUEST,
            "The data has the wrong format and the server can't understand it.",
        )
    try:
        PayloadTypeChecker.Item(**flat_payload)
        for tag_id in tag_ids:
            PayloadTypeChecker.Tag(id=tag_id)
    except ValidationError:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "The posted data has the correct format, but the data is invalid.",
        )

    item = Item(**flat_payload)
    db.session.add(item)
    db.session.flush()

    item_id = item.id
    for tag_id in tag_ids:
        db.session.add(TagOfItem(item_id=item_id, tag_id=tag_id))

    db.session.commit()
    return make_response({"id": item_id})


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
