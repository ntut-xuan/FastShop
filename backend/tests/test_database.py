from __future__ import annotations

from typing import TYPE_CHECKING, no_type_check

import pymysql

from database.util import get_database

if TYPE_CHECKING:
    from flask import Flask


@no_type_check
def test_connection_gotten_during_a_request_is_the_same(app: Flask) -> None:
    with app.app_context():
        db: pymysql.Connection = get_database()

        assert db is get_database()


@no_type_check
def test_connection_closed_automatically_at_the_end_of_request(app: Flask) -> None:
    with app.app_context():
        db: pymysql.Connection = get_database()

    assert db.is_closed()
