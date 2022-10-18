from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from app import create_app

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@pytest.mark.skip("Depends on running database.")
def test_config() -> None:
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_index(client: FlaskClient) -> None:
    response: TestResponse = client.get("/")
    assert b"index.html (a marker for API test)" in response.data
