from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Generator

import pymysql
import pytest

from app import create_app
from database import create_database, get_database

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient

test_cofig: Final[dict[str, Any]] = {
    "TESTING": False,  # integration test, be real with MariaDB
    "MARIADB_USER": "fsta",
    "MARIADB_PASSWORD": "@fsta2022",
    "MARIADB_DATABASE": "fastshop-test",
    "MARIADB_HOST": "fastshop-mariadb-test-1",
}


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app: Flask = create_app(test_cofig)

    with app.app_context():
        create_database()
        insert_test_data()

    yield app

    with app.app_context():
        clean_test_data()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def insert_test_data() -> None:
    data_sql: Final[str] = (Path(__file__).parent / "data.sql").read_text("utf-8")
    executescript(get_database(), data_sql)


def clean_test_data() -> None:
    clean_sql: Final[str] = (Path(__file__).parent / "clean.sql").read_text("utf-8")
    executescript(get_database(), clean_sql)


def executescript(conn: pymysql.Connection, script: str) -> None:
    stmts: tuple[str, ...] = split_sql_script_into_stmts(script)
    for stmt in stmts:
        conn.cursor().execute(stmt)
        conn.commit()


def split_sql_script_into_stmts(sql_script: str) -> tuple[str, ...]:
    """Splits the `sql_script` of multiple semi-colon-delimited (;) statements into tuple of statements."""
    stmts: list[str] = sql_script.split(";")
    return tuple(filter(is_not_empty_stmt, stmts))


def is_not_empty_stmt(stmt: str) -> bool:
    return bool(stmt and stmt != "\n")
