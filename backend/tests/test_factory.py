from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

import pytest
from flask import g

from app import create_app

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_test_config_should_be_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("database.util.connect_database", connect_in_memory_sqlite_db)

    assert not create_app().testing
    assert create_app(test_config={"TESTING": True}).testing


def test_get_index_should_response_content_of_index_html(client: FlaskClient) -> None:
    response: TestResponse = client.get("/")

    assert b"index.html (a marker for API test)" in response.data


def connect_in_memory_sqlite_db() -> None:
    g.db = sqlite3.connect(":memory:")
