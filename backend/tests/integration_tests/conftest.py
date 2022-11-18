from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Final, Generator
from urllib.parse import quote

import pytest

from app import create_app
from database import create_db, db

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app(request: pytest.FixtureRequest) -> Generator[Flask, None, None]:
    def clean() -> None:
        with app.app_context():
            clean_test_data()

    request.addfinalizer(clean)  # cleaned even though the test failed

    app: Flask = create_app(
        {
            "TESTING": False,  # integration test, be real with MariaDB
            "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://fsta:{password}@mariadb-test:3306/fastshop-test".format(
                password=quote("@fsta2022")
            ),
        }
    )

    with app.app_context():
        create_db()
        insert_test_data()

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def insert_test_data() -> None:
    data_sql: str = (Path(__file__).parent / "data.sql").read_text("utf-8")
    executescript(db, data_sql)


def clean_test_data() -> None:
    clean_sql: Final[str] = (Path(__file__).parent / "clean.sql").read_text("utf-8")
    executescript(db, clean_sql)


def executescript(db_, script: str) -> None:
    stmts: tuple[str, ...] = split_sql_script_into_stmts(script)
    for stmt in stmts:
        db_.session.execute(db_.text(stmt))
        db_.session.commit()


def split_sql_script_into_stmts(sql_script: str) -> tuple[str, ...]:
    """Splits the `sql_script` of multiple semi-colon-delimited (;) statements into tuple of statements."""
    stmts: list[str] = sql_script.split(";")
    return tuple(filter(is_not_empty_stmt, stmts))


def is_not_empty_stmt(stmt: str) -> bool:
    return bool(stmt and stmt != "\n")
