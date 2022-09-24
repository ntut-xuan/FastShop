from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pymysql

from flask import g

if TYPE_CHECKING:
    from flask import Flask


def init_database_of_app(app: Flask) -> None:
    with app.app_context():
        connect_database()
    app.teardown_appcontext(close_db)


def get_database() -> pymysql.Connection:
    if not _is_connected():
        connect_database()
    return cast(
        pymysql.Connection, g.db
    )  # we know the type should be `Connection` while inferred to `Any`


def close_db(error: BaseException | None = None) -> None:
    if _is_connected():
        db = g.pop("db")
        db.close()


def connect_database() -> None:
    g.db = pymysql.connect(
        host="fastshop-mariadb-1",
        user="fsa",
        password="@fsa2022",
        database="fastshop",
    )


def _is_connected() -> bool:
    return "db" in g
