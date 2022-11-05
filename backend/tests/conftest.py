from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Generator

import pytest
from flask import current_app, g

from app import create_app
from database import get_database

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app(monkeypatch: pytest.MonkeyPatch) -> Generator[Flask, None, None]:
    db_fd, db_path = tempfile.mkstemp()
    monkeypatch.setattr(
        "database.connect_database",
        lambda: connect_sqlite_database(db_path),
    )
    app: Flask = create_app({"TESTING": True})
    with app.app_context():
        create_sqlite_database()
        insert_test_data()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def insert_test_data() -> None:
    data_sql: str = (Path(__file__).parent / "data.sql").read_text("utf-8")
    get_database().cursor().executescript(data_sql)


def create_sqlite_database() -> None:
    db = get_database()
    with current_app.open_resource("schema.test.sql") as f:
        db.cursor().executescript(f.read().decode("utf-8"))  # type: ignore # f.read() is "bytes", not "str"
        db.commit()


def connect_sqlite_database(db_path: str) -> None:
    g.db = sqlite3.connect(db_path)
