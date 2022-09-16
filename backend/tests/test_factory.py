from __future__ import annotations
from typing import TYPE_CHECKING

from app import create_app

if TYPE_CHECKING:
    from flask.testing import FlaskClient, TestResponse


def test_config() -> None:
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_index(client: FlaskClient) -> None:
    response: TestResponse = client.get("/")
    assert response.data == b"Hello World"
