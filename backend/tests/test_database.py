from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, Any, Iterable, no_type_check

import pytest

from database.util import get_database, _map_names_to_values

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


def test_map_names_to_values() -> None:
    names: list[str] = ["id", "name", "age"]
    values: list[tuple[Any, ...]] = [(1, "some_name", 20), (2, "other_name", 19)]

    named_values: list[dict[str, Any]] = _map_names_to_values(names, values)

    assert len(named_values) == 2
    someone: dict[str, Any] = named_values[0]
    assert someone["id"] == 1
    assert someone["name"] == "some_name"
    assert someone["age"] == 20
    other_one: dict[str, Any] = named_values[1]
    assert other_one["id"] == 2
    assert other_one["name"] == "other_name"
    assert other_one["age"] == 19
