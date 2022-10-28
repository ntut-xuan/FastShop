from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pymysql
from flask import current_app, g

if TYPE_CHECKING:
    from flask import Flask


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


def _is_connected() -> bool:
    return "db" in g
