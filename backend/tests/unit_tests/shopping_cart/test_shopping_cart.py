from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from shopping_cart.route import fetch_user_id_from_jwt_token

if TYPE_CHECKING:
    from http.cookiejar import Cookie, CookieJar
    from flask import Flask
    from flask.testing import FlaskClient


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


def _get_cookies(cookie_jar: CookieJar | None) -> tuple[Cookie, ...]:
    if cookie_jar is None:
        return tuple()
    return tuple(cookie for cookie in cookie_jar)
