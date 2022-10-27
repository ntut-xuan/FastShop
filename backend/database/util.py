from __future__ import annotations

from typing import TYPE_CHECKING, Any, Iterable

from database import get_database

if TYPE_CHECKING:
    import pymysql
    from pymysql.cursors import Cursor


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
