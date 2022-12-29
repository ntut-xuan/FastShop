from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

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


def test_get_items_list_should_respond_content_of_item_list_html(
    client: FlaskClient,
) -> None:
    response: TestResponse = client.get("/items_list")

    assert b"item_list.html (a marker for API test)" in response.data


@pytest.mark.parametrize(argnames="item_id", argvalues=("1", "10", "99"))
def test_get_items_list_by_id_with_any_id_should_respond_content_of_item_detail_html(
    client: FlaskClient, item_id: str
) -> None:
    response: TestResponse = client.get(f"/items_list/{item_id}")

    assert b"item_detail.html (a marker for API test)" in response.data


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
                    "description": "This is an apple.",
                    "original": 30,
                    "discount": 25,
                    "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
                },
                {
                    "id": 2,
                    "name": "tilapia",
                    "count": 3,
                    "description": "This is a tilapia.",
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
    ) -> None:
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "description": "Entropy is so dian.",
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        item_id: int = response_payload["id"]
        with app.app_context():
            item: Item | None = db.session.get(Item, item_id)  # type: ignore[attr-defined]
            assert item is not None
            assert item.avatar == payload["avatar"]
            assert item.count == payload["count"]
            assert item.description == payload["description"]
            assert item.discount == payload["price"]["discount"]
            assert item.original == payload["price"]["original"]
            assert item.name == payload["name"]

    def test_with_correct_payload_should_add_tag_of_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, build_tags: None
    ) -> None:
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "description": "Entropy is so dian.",
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        item_id: int = response_payload["id"]
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

    def test_with_wrong_content_type_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = logged_in_client.post(
            "/items", data="Hello", headers={"content-type": "text/plain"}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_incorrect_data_field_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient
    ) -> None:
        payload: dict[str, Any] = {"invalid_column": "invalid_value"}

        response: TestResponse = logged_in_client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_incorrect_data_type_payload_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient
    ) -> None:
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": "44",  # count should be integer, not string.
            "description": "Entropy is so dian.",
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_no_login_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, build_tags: None
    ) -> None:
        payload: dict[str, Any] = {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "description": "Entropy is so dian.",
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_missing_data_field_should_return_http_status_code_unauthorized(
        self, logged_in_client: FlaskClient, build_tags: None
    ) -> None:
        payload: dict[str, Any] = {
            "count": 44,
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [33, 44],
        }

        response: TestResponse = logged_in_client.post("/items", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST


class TestGetItemsByIdRoute:
    def test_with_exists_id_should_respond_item_payload(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "This is an apple.",
            "price": {"discount": 25, "original": 30},
            "tags": [{"id": 1, "name": "fruit"}, {"id": 3, "name": "grocery"}],
        }

        response: TestResponse = client.get("/items/1")

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        assert response_payload == expected_item_payload

    def test_with_absent_id_should_return_http_status_code_forbidden(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.get("/items/48763")

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestPutItemsByIdRoute:
    def has_equal_item_and_excepted_item_payload(
        self, item_id: int, expected_item_payload: dict[str, Any]
    ) -> bool:
        """
        Has to be called with the app context.

        Args:
            item_id: the id of the item to be compared.
            expected_item_payload: the payload which indicates the expected field values.
        """
        item: Item = db.session.get(Item, item_id)  # type: ignore[attr-defined]
        tag_ids: list[int] = (
            db.session.execute(
                db.select(TagOfItem.tag_id).where(TagOfItem.item_id == item_id)
            )
            .scalars()
            .all()
        )
        tag_ids_from_excepted_item_payload: list[int] = [
            tag["id"] for tag in expected_item_payload["tags"]
        ]

        return (
            item.avatar == expected_item_payload["avatar"]
            and item.count == expected_item_payload["count"]
            and item.name == expected_item_payload["name"]
            and item.original == expected_item_payload["price"]["original"]
            and item.discount == expected_item_payload["price"]["discount"]
            and sorted(tag_ids) == sorted(tag_ids_from_excepted_item_payload)
        )

    def test_with_correct_payload_should_update_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "entropy",
            "count": 3,
            "description": "Entropy is so dian.",
            "price": {"discount": 60, "original": 40},
            "tags": [{"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "avatar": expected_item_payload["avatar"],
            "name": expected_item_payload["name"],
            "count": expected_item_payload["count"],
            "description": expected_item_payload["description"],
            "price": expected_item_payload["price"],
            "tags": [tag_dict["id"] for tag_dict in expected_item_payload["tags"]],
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            assert self.has_equal_item_and_excepted_item_payload(
                1, expected_item_payload
            )

    def test_with_only_price_payload_should_update_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "Entropy is so dian.",
            "price": {"discount": 50, "original": 40},
            "tags": [{"id": 1, "name": "fruit"}, {"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "price": expected_item_payload["price"],
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            assert self.has_equal_item_and_excepted_item_payload(
                1, expected_item_payload
            )

    def test_with_only_original_price_payload_should_update_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "Entropy is so dian.",
            "price": {"discount": 25, "original": 40},
            "tags": [{"id": 1, "name": "fruit"}, {"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "price": {"original": expected_item_payload["price"]["original"]},
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            assert self.has_equal_item_and_excepted_item_payload(
                1, expected_item_payload
            )

    def test_with_only_discount_price_payload_should_update_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "This is an apple.",
            "price": {"discount": 29, "original": 30},
            "tags": [{"id": 1, "name": "fruit"}, {"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "price": {"discount": expected_item_payload["price"]["discount"]},
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            assert self.has_equal_item_and_excepted_item_payload(
                1, expected_item_payload
            )

    def test_with_only_tag_payload_should_update_item_to_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "This is an apple.",
            "price": {"discount": 25, "original": 30},
            "tags": [{"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "tags": [tag_dict["id"] for tag_dict in expected_item_payload["tags"]],
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            assert self.has_equal_item_and_excepted_item_payload(
                1, expected_item_payload
            )

    def test_with_wrong_content_type_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = logged_in_client.put(
            "/items/1", data="Hello", headers={"content-type": "text/plain"}
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_absent_tag_id_payload_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        absent_tag_id = 48763
        update_item_payload: dict[str, Any] = {
            "tags": [absent_tag_id],
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_incorrect_data_type_payload_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        update_item_payload: dict[str, Any] = {
            "count": "some_count",
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_incorrect_data_field_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        update_item_payload: dict[str, Any] = {
            "invalid_field": "invalid_value",
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_payload_contains_id_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        update_item_payload: dict[str, Any] = {
            "id": 49,
        }

        response: TestResponse = logged_in_client.put(
            "/items/1", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_absent_id_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "entropy",
            "count": 3,
            "description": "Entropy is so dian.",
            "price": {"discount": 60, "original": 40},
            "tags": [{"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "avatar": expected_item_payload["avatar"],
            "name": expected_item_payload["name"],
            "count": expected_item_payload["count"],
            "description": expected_item_payload["description"],
            "price": expected_item_payload["price"],
            "tags": [tag_dict["id"] for tag_dict in expected_item_payload["tags"]],
        }

        response: TestResponse = logged_in_client.put(
            "/items/48763", json=update_item_payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_no_login_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        expected_item_payload: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "id": 1,
            "name": "entropy",
            "count": 3,
            "description": "Entropy is so dian.",
            "price": {"discount": 60, "original": 40},
            "tags": [{"id": 3, "name": "grocery"}],
        }
        update_item_payload: dict[str, Any] = {
            "avatar": expected_item_payload["avatar"],
            "name": expected_item_payload["name"],
            "count": expected_item_payload["count"],
            "description": expected_item_payload["description"],
            "price": expected_item_payload["price"],
            "tags": [tag_dict["id"] for tag_dict in expected_item_payload["tags"]],
        }

        response: TestResponse = client.put("/items/1", json=update_item_payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestDeleteItemsByIdRoute:
    def test_with_exists_id_should_delete_the_item_in_database(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = logged_in_client.delete("/items/1")

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            item: Item | None = db.session.get(Item, 1)  # type: ignore[attr-defined]
            assert item is None

    def test_with_absent_id_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient
    ) -> None:
        absent_id = 48763
        response: TestResponse = logged_in_client.delete(f"/items/{absent_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_no_login_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = client.delete("/items/1")

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestGetItemsCountByIdRoute:
    def test_with_exists_id_should_respond_correct_count(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        expected_payload: dict[str, Any] = {
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "This is an apple",
            "original": 30,
            "discount": 25,
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
        }

        response: TestResponse = logged_in_client.get("/items/1/count")

        assert response.status_code == HTTPStatus.OK
        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        assert response_payload["count"] == expected_payload["count"]

    def test_with_absent_id_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        absent_id = 44

        response: TestResponse = logged_in_client.get(f"/items/{absent_id}/count")

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestGetItemsRoute:
    def test_with_empty_tag_item_in_database_should_respond_correct_payload(
        self, app: Flask, client: FlaskClient
    ) -> None:
        item_data: dict[str, Any] = {
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
            "count": 10,
            "description": "This is an apple.",
            "id": 1,
            "name": "apple",
            "original": 30,
            "discount": 25,
        }
        excepted_payload: list[dict[str, Any]] = [
            {
                "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
                "count": 10,
                "description": "This is an apple.",
                "id": 1,
                "name": "apple",
                "price": {
                    "original": 30,
                    "discount": 25,
                },
                "tags": [],
            }
        ]
        with app.app_context():
            item = Item(**item_data)
            db.session.add(item)
            db.session.commit()

        response: TestResponse = client.get("/items")

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        assert response_payload == excepted_payload

    def test_with_route_should_respond_correct_payload(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        excepted_payload: list[dict[str, Any]] = [
            {
                "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
                "count": 10,
                "description": "This is an apple.",
                "id": 1,
                "name": "apple",
                "price": {
                    "original": 30,
                    "discount": 25,
                },
                "tags": [{"id": 1, "name": "fruit"}, {"id": 3, "name": "grocery"}],
            },
            {
                "avatar": "xx-S0m3-aVA7aR-0f-ti1a9iA-xx",
                "count": 3,
                "description": "This is a tilapia.",
                "id": 2,
                "name": "tilapia",
                "price": {
                    "original": 50,
                    "discount": 45,
                },
                "tags": [{"id": 2, "name": "fish"}, {"id": 3, "name": "grocery"}],
            },
        ]

        response: TestResponse = client.get("/items")

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        assert response_payload == excepted_payload
