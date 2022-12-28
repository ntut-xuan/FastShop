from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@pytest.fixture
def logged_in_client(client: FlaskClient) -> FlaskClient:
    client.post("/login", json={"e-mail": "test@email.com", "password": "test"})
    return client


class TestGetUserRoute:
    def test_when_logged_in_should_respond_profile_of_current_user(
        self, logged_in_client: FlaskClient
    ) -> None:
        profile_of_current_user: dict[str, Any] = {
            "e-mail": "test@email.com",
            "firstname": "Han-Xuan",
            "lastname": "Huang",
            "birthday": "2022-10-24",
            "gender": 0,
        }

        response: TestResponse = logged_in_client.get("/user")

        assert response.status_code == HTTPStatus.OK
        payload: dict[str, Any] | None = response.json
        assert payload is not None
        assert payload == profile_of_current_user

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.get("/user")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}


def test_get_with_authorized_account_should_response_content_of_profile_html(
    logged_in_client: FlaskClient,
) -> None:
    resp: TestResponse = logged_in_client.get("/profile")

    assert b"<!-- user_profile.html (a marker for API test) -->" in resp.data


def test_get_with_unauthorized_account_should_response_content_of_login_html(
    client: FlaskClient,
) -> None:
    resp: TestResponse = client.get("/profile", follow_redirects=True)

    assert b"<!-- login.html (a marker for API test) -->" in resp.data
