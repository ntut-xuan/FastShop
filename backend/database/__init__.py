from __future__ import annotations

from typing import TYPE_CHECKING, Final, cast

import click
import pymysql
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

if TYPE_CHECKING:
    from flask import Flask

db: Final[SQLAlchemy] = SQLAlchemy()

# For SQLAlchemy.create_all to know what to create.
# NOTE: imports after the creation of "db" to resolve circular import
from models import *


@click.command("create-db")
def create_db_command() -> None:
    """For flask-sqlalchemy."""
    create_db()
    click.echo("Created the database.")


def create_db() -> None:
    """For flask-sqlalchemy."""
    with current_app.app_context():
        db.create_all()


def connect_database_for_app(app: Flask) -> None:
    with app.app_context():
        connect_database()
    app.teardown_appcontext(close_db)


def create_database() -> None:
    db: pymysql.Connection = get_database()
    with current_app.open_resource("schema.sql") as f:
        db.cursor().execute(f.read().decode("utf-8"))  # type: ignore # f.read() is "bytes", not "str"
        db.commit()


def get_database() -> pymysql.Connection:
    if not _is_connected():
        connect_database()
    return cast(
        pymysql.Connection, g.db
    )  # we know the type should be `Connection` while inferred to `Any`


def connect_database() -> None:
    g.db = pymysql.connect(
        host=current_app.config["MARIADB_HOST"],
        user=current_app.config["MARIADB_USER"],
        password=current_app.config["MARIADB_PASSWORD"],
        database=current_app.config["MARIADB_DATABASE"],
    )


def close_db(error: BaseException | None = None) -> None:
    if _is_connected():
        db = g.pop("db")
        db.close()


def _is_connected() -> bool:
    return "db" in g
