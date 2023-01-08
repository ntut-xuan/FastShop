from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import pytest

from database import db
from models import Item, ShoppingCart, Tag, TagOfItem
from shopping_cart.route import fetch_user_id_from_jwt_token

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


def _get_cookies(cookie_jar: CookieJar | None) -> tuple[Cookie, ...]:
    if cookie_jar is None:
        return tuple()
    return tuple(cookie for cookie in cookie_jar)
