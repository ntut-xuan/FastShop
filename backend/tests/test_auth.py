from __future__ import annotations
from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_invalid_data_on_login_has_status_bad_request(client: FlaskClient) -> None:
    invalid_data: dict[str, str] = {"uriah": "garbage"}

    resp: TestResponse = client.post("/login", json=invalid_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_invalid_email_on_login_has_status_unprocessable_entity(
    client: FlaskClient,
) -> None:
    invalid_email: str = "t109590031@ntut@org@tw"
    data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

    resp: TestResponse = client.post("/login", json=data)

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
