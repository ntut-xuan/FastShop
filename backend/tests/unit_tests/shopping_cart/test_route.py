from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy import func

from src.database import db
from src.models import Item, ShoppingCart, Tag, TagOfItem

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


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
                {
                    "id": 3,
                    "name": "tomato",
                    "count": 45,
                    "description": "This is a tomato.",
                    "original": 40,
                    "discount": 35,
                    "avatar": "xx-S0m3-aVA7aR-0f-t0nnat0-xx",
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
        db.session.execute(
            db.insert(ShoppingCart),
            [
                {"user_id": 1, "item_id": 1, "count": 5},
                {"user_id": 1, "item_id": 2, "count": 8},
                {"user_id": 2, "item_id": 2, "count": 7},
            ],
        )
        db.session.commit()


class TestGetShoppingCartRoute:
    def test_with_logged_in_client_should_respond_excepted_response(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        excepted_response: dict[str, Any] = {
            "count": 2,
            "items": [
                {
                    "count": 5,
                    "id": 1,
                    "price": 25,
                },
                {
                    "count": 8,
                    "id": 2,
                    "price": 45,
                },
            ],
            "price": 485,  # 5*25 + 8*45 = 485
        }

        response: TestResponse = logged_in_client.get("shopping_cart")

        response_payload: dict[str, Any] | None = response.json
        assert response_payload == excepted_response

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = client.get("shopping_cart")

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestPostShoppingCartItemRoute:
    def test_with_logged_in_client_should_add_item_to_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": 5, "id": 3}

        response: TestResponse = logged_in_client.post(
            "shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            item_count: int = db.session.execute(
                db.select([func.count()]).where(
                    ShoppingCart.user_id == 1,  # The user with test@mail.com UID is 1.
                    ShoppingCart.item_id == 3,
                )
            ).scalar()
            assert item_count == 1

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": 5, "id": 3}

        response: TestResponse = client.post("shopping_cart/item", json=request_payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_invalid_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, str] = {"xuan": "idiot"}

        response: TestResponse = logged_in_client.post(
            "shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_data_type_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, Any] = {"id": 3, "count": "10"}

        response: TestResponse = logged_in_client.post(
            "shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_item_already_exists_in_cart_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"id": 2, "count": 10}

        response: TestResponse = logged_in_client.post(
            "shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_exits_item_id_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"id": 47, "count": 10}

        response: TestResponse = logged_in_client.post(
            "shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN


class TestDeleteShoppingCartRoute:
    def test_with_logged_in_client_should_absent_the_shopping_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = logged_in_client.delete("/shopping_cart")

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            item_count: int = db.session.execute(
                db.select([func.count()]).where(
                    ShoppingCart.user_id == 1
                )  # The user with test@mail.com UID is 1.
            ).scalar()
            assert item_count == 0

    def test_with_logged_in_client_should_raise_http_status_code_unauthorized(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        response: TestResponse = client.delete("/shopping_cart")

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestPutShoppingCartItemRoute:
    def test_with_logged_in_client_should_update_item_in_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": 5, "id": 2}

        response: TestResponse = logged_in_client.put(
            "/shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            items_count: int = (
                db.session.execute(
                    db.select(ShoppingCart.count).where(
                        ShoppingCart.user_id
                        == 1,  # The user with test@mail.com UID is 1.
                        ShoppingCart.item_id == 2,
                    )
                )
                .scalars()
                .one()
            )
            assert items_count == 5

    def test_set_item_count_to_zero_with_logged_in_client_should_remove_item_in_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": 0, "id": 2}

        response: TestResponse = logged_in_client.put(
            "/shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.OK
        with app.app_context():
            removed_item: ShoppingCart | None = ShoppingCart.query.filter_by(
                item_id=2, user_id=1
            ).first()
            not_removed_item: ShoppingCart | None = ShoppingCart.query.filter_by(
                item_id=1, user_id=1
            ).first()
            assert removed_item is None
            assert not_removed_item is not None

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": 5, "id": 2}

        response: TestResponse = client.put("/shopping_cart/item", json=request_payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_wrong_format_payload_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, str] = {"xuan": "idiot"}

        response: TestResponse = logged_in_client.put(
            "/shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_data_type_payload_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, Any] = {"count": "5", "id": 2}

        response: TestResponse = logged_in_client.put(
            "/shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_not_exists_in_cart_item_payload_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": 5, "id": 3}

        response: TestResponse = logged_in_client.put(
            "/shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_negative_count_item_payload_should_return_http_status_code_unprocessable_entity(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"count": -5, "id": 2}

        response: TestResponse = logged_in_client.put(
            "/shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_not_exits_item_id_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, setup_item: None
    ) -> None:
        request_payload: dict[str, int] = {"id": 47, "count": 10}

        response: TestResponse = logged_in_client.put(
            "shopping_cart/item", json=request_payload
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
