from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, cast

import pytest

from database import db
from models import Item, Tag, TagOfItem

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@pytest.fixture
def build_tags(app: Flask) -> None:
    with app.app_context():
        db.session.add(Tag(id="33", name="dian"))
        db.session.add(Tag(id="44", name="more-dian"))
        db.session.commit()


@pytest.fixture
def logged_in_client(client: FlaskClient) -> FlaskClient:
    client.post("/login", json={"e-mail": "test@email.com", "password": "test"})
    return client


@pytest.fixture
def setup_item(app: Flask) -> None:
    with app.app_context():
        db.session.execute(
            db.insert(Item),
            [
                {
                    "id": 1,
                    "name": "apple",
                    "count": 10,
                    "original": 30,
                    "discount": 25,
                    "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
                },
                {
                    "id": 2,
                    "name": "tilapia",
                    "count": 3,
                    "original": 50,
                    "discount": 45,
                    "avatar": "xx-S0m3-aVA7aR-0f-ti1a9iA-xx",
                },
            ],
        )
        db.session.execute(
            db.insert(Tag),
            [
                {"id": 1, "name": "fruit"},
                {"id": 2, "name": "fish"},
                {"id": 3, "name": "grocery"},
            ],
        )
        db.session.execute(
            db.insert(TagOfItem),
            [
                {"item_id": 1, "tag_id": 1},
                {"item_id": 2, "tag_id": 2},
                {"item_id": 1, "tag_id": 3},
                {"item_id": 2, "tag_id": 3},
            ],
        )
        db.session.commit()


class TestPostItemsRoute:
    def test_with_correct_payload_should_add_to_database(
        self, app: Flask, logged_in_client: FlaskClient, build_tags: None
    ):
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        response_payload = cast(dict, response.json)
        item_id = response_payload["id"]
        with app.app_context():
            item: Item | None = db.session.get(Item, item_id)  # type: ignore[attr-defined]
            assert item is not None
            assert item.avatar == payload["avatar"]
            assert item.count == payload["count"]
            assert item.discount == payload["price"]["discount"]
            assert item.original == payload["price"]["original"]
            assert item.name == payload["name"]

    def test_with_correct_payload_should_add_tag_of_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, build_tags: None
    ):
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        response_payload = cast(dict, response.json)
        item_id = response_payload["id"]
        with app.app_context():
            tags_of_item: list[TagOfItem] = (
                db.session.execute(
                    db.select(TagOfItem).where(TagOfItem.item_id == item_id)
                )
                .scalars()
                .all()
            )
            assert len(tags_of_item) == len(payload["tags"])
            assert tags_of_item[0].tag_id in payload["tags"]
            assert tags_of_item[1].tag_id in payload["tags"]

    def test_with_incorrect_data_field_payload_should_return_http_status_code_bad_request(
        self,
        logged_in_client: FlaskClient,
    ):
        payload: dict[str, Any] = {"invalid_column": "invalid_value"}

        response: TestResponse = logged_in_client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_incorrect_data_type_payload_should_return_http_status_code_unprocessable_entity(
        self,
        logged_in_client: FlaskClient,
    ):
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": "44",  # count should be integer, not string.
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_no_login_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, build_tags: None
    ):
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestGetItemsRoute:
    def test_with_exists_id_should_respond_item_payload(
        self, client: FlaskClient, setup_item: None
    ):
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "apple",
            "count": 10,
            "price": {"discount": 25, "original": 30},
            "tags": [{"id": 1, "name": "fruit"}, {"id": 3, "name": "grocery"}],
        }
        response: TestResponse = client.get("/items/1")
        response_payload: dict[str, Any] = cast(dict, response.json)

        assert response_payload == expected_item_payload

    def test_with_absent_id_should_return_http_status_code_forbidden(
        self, client: FlaskClient
    ):
        response: TestResponse = client.get("/items/48763")

        assert response.status_code == HTTPStatus.FORBIDDEN
