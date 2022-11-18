from __future__ import annotations

from typing import Final

import click
from flask import current_app
from flask_sqlalchemy import SQLAlchemy


db: Final[SQLAlchemy] = SQLAlchemy()

# For SQLAlchemy.create_all to know what to create.
# NOTE: imports after the creation of "db" to resolve circular import
from models import User


@click.command("create-db")
def create_db_command() -> None:
    """For flask-sqlalchemy."""
    create_db()
    click.echo("Created the database.")


def create_db() -> None:
    """For flask-sqlalchemy."""
    with current_app.app_context():
        db.create_all()
