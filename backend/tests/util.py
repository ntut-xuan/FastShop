from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

import pytest

if TYPE_CHECKING:
    from flask_sqlalchemy import SQLAlchemy


def executescript(db: SQLAlchemy, script: str) -> None:
    """Each SQL statements in `script` should be semi-colon-delimited (;)."""
    stmts: tuple[str, ...] = _split_sql_script_into_stmts(script)
    for stmt in stmts:
        db.session.execute(db.text(stmt))
        db.session.commit()


@contextmanager
def assert_not_raise(exception: type[BaseException]) -> Generator[None, None, None]:
    try:
        yield
    except exception:
        pytest.fail(f"DID RAISE {exception}")


def _split_sql_script_into_stmts(sql_script: str) -> tuple[str, ...]:
    """Splits the `sql_script` of multiple semi-colon-delimited (;) statements into tuple of statements."""
    stmts: list[str] = sql_script.split(";")
    return tuple(filter(_is_not_empty_stmt, stmts))


def _is_not_empty_stmt(stmt: str) -> bool:
    return bool(stmt and stmt != "\n")
