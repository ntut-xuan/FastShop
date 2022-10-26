from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable, cast

import pymysql
from flask import current_app, g

if TYPE_CHECKING:
    from flask import Flask
    from pymysql.cursors import Cursor


def connect_database_for_app(app: Flask) -> None:
    with app.app_context():
        connect_database()
    app.teardown_appcontext(close_db)


def create_database() -> None:
    db: pymysql.Connection = get_database()
    with current_app.open_resource("schema.sql") as f:
        db.cursor().executescript(f.read().decode("utf-8"))  # type: ignore # f.read() is "bytes", not "str"
        db.commit()


def get_database() -> pymysql.Connection:
    if not _is_connected():
        connect_database()
    return cast(
        pymysql.Connection, g.db
    )  # we know the type should be `Connection` while inferred to `Any`


def connect_database() -> None:
    g.db = pymysql.connect(
        host="fastshop-mariadb-1",
        user="fsa",
        password="@fsa2022",
        database="fastshop",
    )


def close_db(error: BaseException | None = None) -> None:
    if _is_connected():
        db = g.pop("db")
        db.close()


def execute_command(command: str, paramter: tuple) -> list[dict[str, Any]]:
    """Executes the command on the database of the current app context.

    Returns:
        A list of results. Each result is represented as a dict with its
        field names being the keys.
    """
    conn: pymysql.Connection = get_database()
    cursor: Cursor = conn.cursor()
    cursor.execute(command, paramter)
    conn.commit()

    named_results: list[dict[str, Any]] = get_results_mapped_by_field_name(cursor)
    cursor.close()

    return named_results


def get_results_mapped_by_field_name(cursor: Cursor) -> list[dict[str, Any]]:
    """
    Returns:
        A list of results held by the `cursor`. Each result is represented as a dict with its
        field names being the keys. The list is empty for executions that do not return rows.
    """
    named_results: list[dict[str, Any]] = []
    if _has_result(cursor):
        field_names: list[str] = _get_field_names(cursor.description)
        results: tuple[tuple, ...] = cursor.fetchall()
        named_results = _map_names_to_values(field_names, results)
    return named_results


def _is_connected() -> bool:
    return "db" in g


def _get_field_names(cursor_description: tuple[str, ...]) -> list[str]:
    """
    DB API returns a 7-tuple for each column where the last six items of each tuple are None,
    which is useless.
    """
    return [name[0] for name in cursor_description]


def _map_names_to_values(
    names: Iterable[str], values: Iterable[Iterable[Any]]
) -> list[dict[str, Any]]:
    named_results: list[dict[str, Any]] = []
    for data in values:
        named_result: dict[str, Any] = dict(zip(names, list(data)))
        named_results.append(named_result)
    return named_results


def _has_result(cursor: Cursor) -> bool:
    """Returns whether the latest execution on `cursor` produces results."""
    # cursor.desciption is None for executions that do not return rows
    # or if the cursor has not had an execution invoked yet.
    return cursor.description is not None
