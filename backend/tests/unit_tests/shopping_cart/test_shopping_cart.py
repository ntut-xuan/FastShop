from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import pytest

from database import db
from models import Item, ShoppingCart, Tag, TagOfItem
from shopping_cart.route import fetch_user_id_from_jwt_token
from sqlalchemy import func

if TYPE_CHECKING:
    from http.cookiejar import Cookie, CookieJar
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


def test_user_id_fetch_function_with_logined_client_should_return_user_id(
    app: Flask, logged_in_client: FlaskClient
):
    with app.app_context():
        cookies: tuple[Cookie, ...] = _get_cookies(logged_in_client.cookie_jar)
        (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
        assert jwt_cookie.value is not None
        jwt_token = jwt_cookie.value

        user_id: int = fetch_user_id_from_jwt_token(jwt_token)

        assert user_id == 1  # The user with test@mail.com UID is 1.


class TestGetShoppingCart:
    def test_with_logged_in_client_should_respond_excepted_response(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        excepted_response = {
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
        with app.app_context():

            response: TestResponse = logged_in_client.get("shopping_cart")

            response_payload: dict[str, Any] | None = response.json
            assert response_payload == excepted_response

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_item: None
    ):
        with app.app_context():

            response: TestResponse = client.get("shopping_cart")

            assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestPostShoppingCartItem:
    def test_with_logged_in_client_should_add_item_to_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": 5, "id": 3}
        with app.app_context():

            response: TestResponse = logged_in_client.post(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.OK
            item_count = db.session.execute(
                db.select([func.count()]).where(
                    ShoppingCart.user_id == 1,  # The user with test@mail.com UID is 1.
                    ShoppingCart.item_id == 3,
                )
            ).scalar()
            assert item_count == 1

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": 5, "id": 3}
        with app.app_context():

            response: TestResponse = client.post(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_invalid_payload_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"xuan": "idiot"}
        with app.app_context():

            response: TestResponse = logged_in_client.post(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_data_type_should_return_http_status_code_unprocessable_entity(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"id": 3, "count": "10"}
        with app.app_context():

            response: TestResponse = logged_in_client.post(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_item_already_exists_in_cart_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"id": 2, "count": 10}
        with app.app_context():

            response: TestResponse = logged_in_client.post(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.FORBIDDEN

    def test_with_not_exits_item_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"id": 47, "count": 10}
        with app.app_context():

            response: TestResponse = logged_in_client.post(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.FORBIDDEN


class TestDeleteShoppingCart:
    def test_with_logged_in_client_should_absent_the_shopping_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        with app.app_context():

            response: TestResponse = logged_in_client.delete("/shopping_cart")

            assert response.status_code == HTTPStatus.OK
            item_count = db.session.execute(
                db.select([func.count()]).where(
                    ShoppingCart.user_id == 1
                )  # The user with test@mail.com UID is 1.
            ).scalar()
            assert item_count == 0

    def test_with_logged_in_client_should_raise_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_item: None
    ):
        with app.app_context():

            response: TestResponse = client.delete("/shopping_cart")

            assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestPutShoppingCartItem:
    def test_with_logged_in_client_should_update_item_in_cart(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": 5, "id": 2}
        with app.app_context():

            response: TestResponse = logged_in_client.put(
                "/shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.OK
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

    def test_with_not_logged_in_client_should_return_http_status_code_unauthorized(
        self, app: Flask, client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": 5, "id": 2}
        with app.app_context():

            response: TestResponse = client.put(
                "/shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_with_wrong_format_payload_should_return_http_status_code_bad_request(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"xuan": "idiot"}
        with app.app_context():

            response: TestResponse = logged_in_client.put(
                "/shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_with_invalid_data_type_payload_should_return_http_status_code_unprocessable_entity(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": "5", "id": 2}
        with app.app_context():

            response: TestResponse = logged_in_client.put(
                "/shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_not_exists_in_cart_item_payload_should_return_http_status_code_unprocessable_entity(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": 5, "id": 3}
        with app.app_context():

            response: TestResponse = logged_in_client.put(
                "/shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_negative_count_item_payload_should_return_http_status_code_unprocessable_entity(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"count": -5, "id": 2}
        with app.app_context():

            response: TestResponse = logged_in_client.put(
                "/shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_with_not_exits_item_id_should_return_http_status_code_forbidden(
        self, app: Flask, logged_in_client: FlaskClient, setup_item: None
    ):
        request_payload = {"id": 47, "count": 10}
        with app.app_context():

            response: TestResponse = logged_in_client.put(
                "shopping_cart/item", json=request_payload
            )

            assert response.status_code == HTTPStatus.FORBIDDEN


def _get_cookies(cookie_jar: CookieJar | None) -> tuple[Cookie, ...]:
    if cookie_jar is None:
        return tuple()
    return tuple(cookie for cookie in cookie_jar)
