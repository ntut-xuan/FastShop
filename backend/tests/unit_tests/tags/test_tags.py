from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from database import db
from models import Tag

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_get_tags_should_return_count_0_if_no_existing_tags(
    client: FlaskClient,
) -> None:
    response: TestResponse = client.get("/tags")

    data = cast(dict, response.json)
    count: int = data["count"]
    assert count == 0


def test_get_tags_should_return_all_existing_tags(
    app: Flask, client: FlaskClient
) -> None:
    tags: list[dict[str, Any]] = [
        {"id": 1, "name": "seafood"},
        {"id": 2, "name": "fruit"},
        {"id": 3, "name": "solid food"},
    ]
    with app.app_context():
        db.session.execute(db.insert(Tag), tags)
        db.session.commit()

    response: TestResponse = client.get("/tags")

    assert response.json is not None
    data: dict[str, Any] = response.json
    assert data["count"] == 3
    responded_tags: list[dict[str, Any]] = data["tags"]
    assert responded_tags[0] in tags
    assert responded_tags[1] in tags
    assert responded_tags[2] in tags
