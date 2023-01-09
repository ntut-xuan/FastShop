from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Iterable

from flask import Blueprint, make_response, request
from pydantic import ValidationError

from src.auth.util import verify_login_or_return_401
from src.database import db
from src.item.util import PayloadTypeChecker, flatten_item_payload
from src.models import Item, Tag, TagOfItem
from util import fetch_page, make_single_message_response, route_with_doc

if TYPE_CHECKING:
    from flask import Response
    from sqlalchemy.engine.row import Row
    from sqlalchemy.sql.expression import Delete, Select

item_bp = Blueprint("item", __name__)


@route_with_doc(item_bp, "/items", methods=["GET"])
def fetch_all_items() -> Response:
    tags_of_item: list[Row] = db.session.execute(
        db.select(TagOfItem.item_id, TagOfItem.tag_id, Tag.name)
        .select_from(TagOfItem)
        .join(Tag)
    ).all()
    item_id_to_tags: dict[int, list[dict[str, Any]]] = _map_item_id_to_tags(
        tags_of_item
    )

    items: list[Item] = db.session.execute(db.select(Item)).scalars().all()
    payload: list[dict[str, Any]] = [
        {
            "avatar": item.avatar,
            "count": item.count,
            "description": item.description,
            "id": item.id,
            "name": item.name,
            "price": {
                "discount": item.discount,
                "original": item.original,
            },
            "tags": item_id_to_tags.get(item.id, []),
        }
        for item in items
    ]
    return make_response(payload)


@route_with_doc(item_bp, "/items", methods=["POST"])
@verify_login_or_return_401
def add_item() -> Response:
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

    item_id: int = item.id
    for tag_id in tag_ids:
        db.session.add(TagOfItem(item_id=item_id, tag_id=tag_id))

    db.session.commit()
    return make_response({"id": item_id})


@route_with_doc(item_bp, "/items/<string:id>", methods=["GET"])
def fetch_specific_item(id) -> Response:
    item: Item | None = db.session.get(Item, id)  # type: ignore[attr-defined]

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    tags: list[dict[str, Any]] = _fetch_item_tags_list_from_item_id(item.id)

    item_with_tags_data: dict[str, Any] = {
        "avatar": item.avatar,
        "count": item.count,
        "description": item.description,
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
def update_specific_item(id) -> Response:
    item: Item | None = db.session.get(Item, id)  # type: ignore[attr-defined]
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

    # Since `flatten_item_payload` requires all the fields to be present as a one level dict,
    # we have to flatten some fields first.
    if "price" in payload:
        if "original" in payload["price"]:
            payload["original"] = payload["price"]["original"]
        if "discount" in payload["price"]:
            payload["discount"] = payload["price"]["discount"]
        del payload["price"]

    # validate payload data field
    if (
        not _has_only_allowed_keys(
            payload.keys(), list(item.__dict__.keys()) + ["tags"]
        )
        or "id" in payload.keys()  # you can't update the id
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
def delete_specific_item(id) -> Response:
    item: Item | None = db.session.get(Item, id)  # type: ignore[attr-defined]

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    db.session.delete(item)
    db.session.commit()

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(item_bp, "/items/<string:id>/count", methods=["GET"])
def fetch_count_of_specific_item(id) -> Response:
    item: Item | None = db.session.get(Item, id)  # type: ignore[attr-defined]

    if item is None:
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, "The specific item is absent."
        )

    return make_response({"count": item.count})


@route_with_doc(item_bp, "/items_list/<string:id>", methods=["GET"])
def item_page(id: str) -> str:
    # id is intentionally ignored. Backend does not have to handle.
    return fetch_page("item_detail")


@route_with_doc(item_bp, "/items_list", methods=["GET"])
def item_list_page() -> str:
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


def _setup_tags_relationship_of_item(item_id: int, tags_ids: list[int]) -> None:
    # Step 1. Drop all tags of item if exists.
    delete_tags_stmts: Delete = db.delete(TagOfItem).where(TagOfItem.item_id == item_id)
    db.session.execute(delete_tags_stmts)
    db.session.commit()

    # Step 2. Insert all tags relationship
    for tag_id in tags_ids:
        db.session.add(TagOfItem(item_id=item_id, tag_id=tag_id))
    db.session.commit()


def _map_item_id_to_tags(tags_of_item: list[Row]) -> dict[int, list[dict[str, Any]]]:
    """Maps the list which has duplicate item ids into a dict which item ids are the keys."""
    item_id_to_tags: dict[int, list[dict[str, Any]]] = {}

    for tag_of_item in tags_of_item:
        item_id_to_tags.setdefault(tag_of_item.item_id, []).append(
            {"id": tag_of_item.tag_id, "name": tag_of_item.name}
        )
    return item_id_to_tags


def _has_only_allowed_keys(target: Iterable, allowed: Iterable) -> bool:
    for key in target:
        if key not in allowed:
            return False
    return True


def _is_tags_exist(tags: list[int]) -> bool:
    query_tags: list[Tag] = db.session.query(Tag).filter(Tag.id.in_(tags)).all()
    return len(query_tags) == len(tags)
