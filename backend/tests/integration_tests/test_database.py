from __future__ import annotations

from database import get_database
from typing import TYPE_CHECKING, Any

from database.util import execute_command

if TYPE_CHECKING:
    import pymysql
    from flask import Flask
    from pytest import FixtureRequest


class TestExecuteCommand:
    def test_on_update_should_have_empty_result(self, app: Flask) -> None:
        update_stmt: str = (
            "UPDATE `test_table` SET `password` = %s WHERE `account` = %s;"
        )

        with app.app_context():
            results: list[dict[str, Any]] = execute_command(
                update_stmt, ("#new_password", "my_account")
            )

        assert len(results) == 0

    def test_on_select_should_have_results(self, app: Flask) -> None:
        select_stmt: str = "SELECT * FROM `test_table`;"

        with app.app_context():
            results: list[dict[str, Any]] = execute_command(select_stmt, ())

        assert len(results) == 2

    def test_on_const_select_should_have_results(self, app: Flask) -> None:
        select_stmt: str = "SELECT 1 as `n`;"

        with app.app_context():
            results: list[dict[str, Any]] = execute_command(select_stmt, ())

        assert len(results) == 1
        (result,) = results
        assert result["n"] == 1

    def test_on_delete_should_have_empty_result(self, app: Flask) -> None:
        delete_stmt: str = "DELETE FROM `test_table` WHERE `account` = %s;"

        with app.app_context():
            results: list[dict[str, Any]] = execute_command(
                delete_stmt, ("my_account",)
            )

        assert len(results) == 0

    def test_on_create_should_have_empty_result(
        self, app: Flask, request: FixtureRequest
    ) -> None:
        def drop_new_table() -> None:
            with app.app_context():
                conn: pymysql.Connection = get_database()
                conn.cursor().execute("DROP TABLE IF EXISTS `new_table`;")
                conn.commit()
        request.addfinalizer(
            drop_new_table
        )  # tears down even though the assertion fails

        create_stmt: str = "CREATE TABLE `new_table` (`id` INT PRIMARY KEY);"

        with app.app_context():
            results: list[dict[str, Any]] = execute_command(create_stmt, ())

        assert len(results) == 0
