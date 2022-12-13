from __future__ import annotations

from base64 import b64decode
from typing import TYPE_CHECKING, Any
from os.path import exists

import pytest

from static.util import (
    get_image_byte_from_existing_file,
    has_image_with_specific_id,
)

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_upload_image_should_return_401_if_user_not_login(client: FlaskClient):
    content: str = "data:image/png;base64,..."

    response: TestResponse = client.post(
        "/static/images", data=content, content_type="text/plain"
    )

    assert response.status_code == 401


def test_upload_image_should_store_base64_to_static_file_path(
    app: Flask, client: FlaskClient
):
    base64_image_content = (
        "ZG9lc19ub3RfbWF0dGVy"  # The base64 encode result of "does_not_matter"
    )
    content: str = "data:image/png;base64," + base64_image_content
    client.post(
        "/login",
        json={
            "e-mail": "test@email.com",
            "password": "test",
        },
    )
    with app.app_context():

        response: TestResponse = client.post(
            "/static/images", data=content, content_type="text/plain"
        )
        data_dict: dict[str, Any] = response.json  # type: ignore

        assert response.status_code == 200
        assert has_image_with_specific_id(data_dict["uuid"])
        assert get_image_byte_from_existing_file(data_dict["uuid"]) == b64decode(
            base64_image_content
        )


def test_upload_image_with_invalid_content_should_return_400(client: FlaskClient):
    content: str = "data:image/png;base64,____________=="
    client.post(
        "/login",
        json={
            "e-mail": "test@email.com",
            "password": "test",
        },
    )

    response: TestResponse = client.post(
        "/static/images", data=content, content_type="text/plain"
    )

    assert response.status_code == 400
