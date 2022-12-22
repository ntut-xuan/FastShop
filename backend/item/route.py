from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import Blueprint, make_response, request
from pydantic import ValidationError
from sqlalchemy.engine.row import Row
from sqlalchemy.sql.expression import Delete, Select

from auth.util import verify_login_or_return_401
from database import db
from item.util import PayloadTypeChecker, flatten_item_payload
from models import Item, Tag, TagOfItem
from util import fetch_page, make_single_message_response, route_with_doc

item_bp = Blueprint("item", __name__)


@route_with_doc(item_bp, "/items", methods=["GET"])
def fetch_all_items():
    items: list[Item] = db.session.execute(db.select(Item)).scalars().all()
    tag_of_items: list[Row] = db.session.execute(
        db.select(TagOfItem.item_id, TagOfItem.tag_id, Tag.name)
        .select_from(TagOfItem)
        .join(Tag)
    ).all()

    tags_list_dict_by_item_id: dict[int, list[dict[str, Any]]] = {}

    for tag_of_item in tag_of_items:
        item_id = tag_of_item.item_id
        tag_id = tag_of_item.tag_id
        tag_name = tag_of_item.name

        if item_id not in tags_list_dict_by_item_id:
            tags_list_dict_by_item_id[item_id] = []
        tags_list_dict_by_item_id[item_id].append({"id": tag_id, "name": tag_name})

    item_represent_list: list[dict[str, Any]] = []

    for item in items:
        item_represent_list.append(
            {
                "avatar": item.avatar,
                "count": item.count,
                "id": item.id,
                "name": item.name,
                "price": {
                    "discount": item.discount,
                    "original": item.original,
                },
                "tags": tags_list_dict_by_item_id[item.id],
            }
        )

    return make_response(item_represent_list)


@route_with_doc(item_bp, "/items", methods=["POST"])
@verify_login_or_return_401
def add_item():
    payload: dict[str, Any] | None = request.get_json(silent=True)

    if payload is None or "name" not in payload:
        return make_single_message_response(
            HTTPStatus.BAD_REQUEST,
            "The data has the wrong format and the server can't understand it.",
        )

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
    item: Item | None = db.session.get(Item, id)

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    tags: list[dict[str, Any]] = _fetch_item_tags_list_from_item_id(item.id)

    item_with_tags_data: dict[str, Any] = {
        "avatar": item.avatar,
        "count": item.count,
        "id": item.id,
        "name": item.name,
        "price": {
            "original": item.original,
            "discount": item.discount,
        },
        "tags": tags,
    }

    return make_response(item_with_tags_data)


@route_with_doc(item_bp, "/items/<string:id>", methods=["PUT"])
@verify_login_or_return_401
def update_specific_item(id):
    item: Item | None = db.session.get(Item, id)
    payload: dict[str, Any] | None = request.get_json(silent=True)

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    if payload is None:
        return make_single_message_response(
            HTTPStatus.BAD_REQUEST,
            "The data has the wrong format and the server can't understand it.",
        )

    # Since flatten_item_payload require ALL the field have present.
    # So we need to flat the specific field to complete the flattern action.
    # Flat the price dict, since only price need to flat.
    if "price" in payload:
        if "original" in payload["price"]:
            payload["original"] = payload["price"]["original"]
        if "discount" in payload["price"]:
            payload["discount"] = payload["price"]["discount"]
        del payload["price"]

    # validate payload data field
    item_attributes: list = list(item.__dict__.keys())
    if (
        not _validate_keys(payload.keys(), item_attributes, ["tags"])
        or "id" in payload.keys()
    ):
        return make_single_message_response(
            HTTPStatus.BAD_REQUEST,
            "The data has the wrong format and the server can't understand it.",
        )

    # validate tags exist
    if "tags" in payload and not _is_tags_exist(payload["tags"]):
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "The posted data has the correct format, but the data is invalid.",
        )

    # validate payload data type
    try:
        PayloadTypeChecker.Item(**payload)
        if "tags" in payload:
            for tag_id in payload["tags"]:
                PayloadTypeChecker.Tag(id=tag_id)
    except ValidationError:
        return make_single_message_response(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "The posted data has the correct format, but the data is invalid.",
        )

    # update item column
    for key, value in payload.items():
        setattr(item, key, value)

    # update tags relationship
    if "tags" in payload:
        _setup_tags_relationship_of_item(item.id, payload["tags"])

    db.session.commit()
    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(item_bp, "/items/<string:id>", methods=["DELETE"])
@verify_login_or_return_401
def delete_specific_item(id):
    item: Item | None = db.session.get(Item, id)

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    db.session.delete(item)
    db.session.commit()

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(item_bp, "/items/<string:id>/count", methods=["GET"])
def fetch_count_of_specific_item(id):
    item: Item | None = db.session.get(Item, id)

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    return make_response({"count": item.count})


@route_with_doc(item_bp, "/items_list/<string:id>", methods=["GET"])
def item_page(id: str):
    # id is intentionally ignored. Backend does not have to handle.
    return fetch_page("item_detail")


@route_with_doc(item_bp, "/items_list", methods=["GET"])
def item_list_page():
    return fetch_page("item_list")


def _fetch_item_tags_list_from_item_id(id: int) -> list[dict[str, Any]]:
    tags_join_stmts: Select = (
        db.select(TagOfItem.tag_id, Tag.name)
        .select_from(TagOfItem)
        .join(Tag)
        .where(TagOfItem.item_id == id)
    )
    tags_query_result: list[Row] = db.session.execute(tags_join_stmts).all()

    tags_dict_list: list[dict[str, Any]] = []
    for tags_query in tags_query_result:
        tags_dict_list.append({"id": tags_query.tag_id, "name": tags_query.name})

    return tags_dict_list


def _setup_tags_relationship_of_item(item_id: int, tags_id_list: list[int]):
    # Step 1. Drop all tags of item if exists.
    delete_tags_stmts: Delete = db.delete(TagOfItem).where(TagOfItem.item_id == item_id)
    db.session.execute(delete_tags_stmts)
    db.session.commit()

    # Step 2. Insert all tags relationship
    for tag_id in tags_id_list:
        db.session.add(TagOfItem(item_id=item_id, tag_id=tag_id))
    db.session.commit()


def _validate_keys(target_keys: list, known_keys: list, skip_keys: list) -> bool:
    for key in target_keys:
        if key in skip_keys:
            continue
        if key not in known_keys:
            return False
    return True


def _is_tags_exist(tags: list[int]) -> bool:
    query_tags: list[Tag] = db.session.query(Tag).filter(Tag.id.in_(tags)).all()
    return len(query_tags) == len(tags)
