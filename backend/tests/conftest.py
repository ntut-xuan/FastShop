from __future__ import annotations

import os
import sqlite3
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Generator

import pytest
from flask import g

from app import create_app
from database import create_database, get_database
from database.util import execute_command

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app(monkeypatch: pytest.MonkeyPatch) -> Generator[Flask, None, None]:
    """
    db_fd, db_path = tempfile.mkstemp()

    monkeypatch.setattr(
        "database.connect_database",
        lambda: connect_sqlite_database(db_path),
    )
    """
    app: Flask = create_app({"TESTING": False})

    """
    with app.app_context():
        #create_database()
        #insert_test_data()
    """
    yield app
    """
    os.close(db_fd)
    os.unlink(db_path)
    """
    with app.app_context():
        db = get_database()
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM `test_table`;")
            cursor.execute("DELETE FROM `user`;")
            cursor.execute(
                """
            INSERT INTO `user` (`uid`, `email`, `password`, `firstname`, `lastname`, `gender`, `birthday`)
            VALUES (
                0,
                'test@email.com',
                -- test
                'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff',
                'Han-Xuan',
                'Huang',
                0,
                1666604387  -- 2002-06-25
            ),
            (
                1,
                'other@email.com',
                -- other
                '82a5cfd03cdcb713c8d7dfce41e6f0a92f6dc560e6dda56c11eb1a207aaa7689b07a1de30967fc040f8b0ef0672c1c2ad96fcacb95fb995f52ae5d657c094547',
                'Xuan',
                'Uriah',
                0,
                1666604387  -- 2002-06-25
            );
            """
            )
            cursor.execute(
                "INSERT INTO `test_table` (`account`, `password`) VALUES ('my_account', '#my_password'), ('other_account', '#other_password');"
            )
            cursor.execute("DROP TABLE IF EXISTS `new_table`;")


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def insert_test_data() -> None:
    data_sql: str = (Path(__file__).parent / "data.sql").read_text("utf-8")
    get_database().cursor().executescript(data_sql)


def connect_sqlite_database(db_path: str) -> None:
    g.db = sqlite3.connect(db_path)
