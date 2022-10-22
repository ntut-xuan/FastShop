from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, no_type_check

import pytest

from database.util import get_database

if TYPE_CHECKING:
    from flask import Flask


@no_type_check
def test_connection_gotten_during_a_request_should_be_the_same(app: Flask) -> None:
    with app.app_context():
        db = get_database()

        assert db is get_database()


@no_type_check
def test_connection_should_close_automatically_at_the_end_of_request(
    app: Flask,
) -> None:
    with app.app_context():
        db: sqlite3.Connection = get_database()  # type: ignore  # sqlite in test environment

    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        db.execute("SELECT 1")
