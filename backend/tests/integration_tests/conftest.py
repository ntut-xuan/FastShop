from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Generator
from urllib.parse import quote

import pytest

from app import create_app
from database import create_db, db
from tests.util import executescript

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app: Flask = create_app(
        {
            "TESTING": False,  # integration test, be real with MariaDB
            "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://fsta:{password}@mariadb-test:3306/fastshop-test".format(
                password=quote("@fsta2022")
            ),
            "STATIC_RESOURCE_PATH": "/var/fastshop/image",
        }
    )

    with app.app_context():
        create_db()
        insert_test_data()

    yield app

    with app.app_context():
        db.drop_all()


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
