from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Generator

import pytest

from app import create_app
from src.database import create_db, db
from tests.util import executescript

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    db_fp, db_path = tempfile.mkstemp()
    static_path: str = tempfile.mkdtemp()
    app: Flask = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "STATIC_RESOURCE_PATH": static_path,
        }
    )
    with app.app_context():
        create_db()
        insert_test_data()

    yield app

    os.close(db_fp)
    os.unlink(db_path)
    shutil.rmtree(static_path)


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def logged_in_client(client: FlaskClient) -> FlaskClient:
    client.post("/login", json={"e-mail": "test@email.com", "password": "test"})
    return client


def insert_test_data() -> None:
    data_sql: str = (Path(__file__).parent / "data.sql").read_text("utf-8")
    executescript(db, data_sql)
