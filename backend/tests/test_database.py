from __future__ import annotations
from typing import TYPE_CHECKING

import pymysql
import pytest

from database.util import get_database

if TYPE_CHECKING:
    from flask import Flask


def test_connection_gotten_during_a_request_is_the_same(app: Flask) -> None:
    with app.app_context():
        db: pymysql.Connection = get_database()

        assert db is get_database()


def test_connection_closed_automatically_at_the_end_of_request(app: Flask) -> None:
    with app.app_context():
        db: pymysql.Connection = get_database()

    with pytest.raises(pymysql.err.InterfaceError):
        db.cursor().execute("SELECT 1")
