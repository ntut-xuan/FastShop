from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, Generator

import pytest
from flask import g

from app import create_app

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture(autouse=True)
def monkey_patch_to_use_sqlite_in_test(monkeypatch: pytest.MonkeyPatch) -> None:
    def connect_sqlite_database() -> None:
        g.db = sqlite3.connect(":memory:")

    monkeypatch.setattr("database.util.connect_database", connect_sqlite_database)


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app: Flask = create_app({"TESTING": True})

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
