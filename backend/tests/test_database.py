from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING, Any, no_type_check

import pytest

from database.util import execute_command, get_database, _map_names_to_values

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


def test_execute_command_on_update_should_have_empty_result(app: Flask) -> None:
    update_stmt: str = "UPDATE `test_table` SET `password` = ? WHERE `account` = ?;"

    with app.app_context():
        results: list[dict[str, Any]] = execute_command(
            update_stmt, ("#new_password", "my_account")
        )

    assert len(results) == 0


def test_execute_command_on_select_should_have_results(app: Flask) -> None:
    select_stmt: str = "SELECT * FROM `test_table`;"

    with app.app_context():
        results: list[dict[str, Any]] = execute_command(select_stmt, ())

    assert len(results) == 2


def test_execute_command_on_const_select_should_have_results(app: Flask) -> None:
    select_stmt: str = "SELECT 1 as `n`;"

    with app.app_context():
        results: list[dict[str, Any]] = execute_command(select_stmt, ())

    assert len(results) == 1
    (result,) = results
    assert result["n"] == 1


def test_execute_command_on_delete_should_have_empty_result(app: Flask) -> None:
    delete_stmt: str = "DELETE FROM `test_table` WHERE `account` = ?;"

    with app.app_context():
        results: list[dict[str, Any]] = execute_command(delete_stmt, ("my_account",))

    assert len(results) == 0


def test_execute_command_on_create_should_have_empty_result(app: Flask) -> None:
    create_stmt: str = "CREATE TABLE `new_table` (id INT PRIMARY KEY);"

    with app.app_context():
        results: list[dict[str, Any]] = execute_command(create_stmt, ())

    assert len(results) == 0
