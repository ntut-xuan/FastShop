from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

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


# TODO: this method does more than one thing
def execute_command(command: str, paramter: tuple) -> list:
    # 1. execute command
    conn: pymysql.Connection = get_database()
    cursor: Cursor = conn.cursor()
    cursor.execute(command, paramter)
    conn.commit()

    # 2. combine field with value to a dict
    named_results: list[dict[str, Any]] = []
    if cursor.description != None:
        # mysql may support better named attributes such as `with_rows` to check
        # whether the executed operation could have produced rows,
        # but we only use those defined in DB-API 2.0.

        results: tuple[tuple, ...] = cursor.fetchall()
        field_names: list[str] = _get_field_names(cursor.description)
        for data in results:
            named_result: dict[str, Any] = dict(zip(field_names, list(data)))
            named_results.append(named_result)
    cursor.close()
    return named_results


def close_db(error: BaseException | None = None) -> None:
    if _is_connected():
        db = g.pop("db")
        db.close()


def _is_connected() -> bool:
    return "db" in g


def _get_field_names(cursor_description: tuple[str, ...]) -> list[str]:
    """
    DB API returns a 7-tuple for each column where the last six items of each tuple are None,
    which is useless.
    """
    return [name[0] for name in cursor_description]
