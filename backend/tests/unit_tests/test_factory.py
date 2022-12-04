from __future__ import annotations

from typing import TYPE_CHECKING

from app import create_app

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_test_config_should_be_loaded() -> None:
    assert not create_app().testing
    assert create_app(
        test_config={"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    ).testing


def test_get_index_should_response_content_of_index_html(client: FlaskClient) -> None:
    response: TestResponse = client.get("/")

    assert b"index.html (a marker for API test)" in response.data
