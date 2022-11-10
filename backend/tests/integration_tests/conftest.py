from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

import pytest

from app import create_app
from database import create_database, get_database

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient

test_cofig: dict[str, Any] = {
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
        with get_database().cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO `user` (`email`, `password`, `firstname`, `lastname`, `gender`, `birthday`)
                VALUES (
                    'test@email.com',
                    -- test
                    'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff',
                    'Han-Xuan',
                    'Huang',
                    0,
                    1666604387  -- 2002-06-25
                ),
                (
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
                """
                CREATE TABLE IF NOT EXISTS `test_table` (
                    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
                    `account` TEXT NOT NULL UNIQUE,
                    `password` TEXT NOT NULL
                );
                """
            )
            cursor.execute(
                """
                INSERT INTO `test_table` (`account`, `password`)
                VALUES ('my_account', '#my_password'),
                    ('other_account', '#other_password');
                """
            )
        get_database().commit()

    yield app

    with (app.app_context(), get_database().cursor() as cursor):
        cursor.execute("DROP TABLE IF EXISTS `test_table`;")
        cursor.execute("DROP TABLE IF EXISTS `user`;")
        cursor.execute("DROP TABLE IF EXISTS `new_table`;")
        get_database().commit()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
