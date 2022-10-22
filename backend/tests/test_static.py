from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from app import fetch_page

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_fetch_page(client: FlaskClient) -> None:
    with client.application.app_context():
        page_content: str = fetch_page("index")

    assert "index.html (a marker for API test)" in page_content


def test_get_static_file_should_have_code_OK(client: FlaskClient) -> None:
    response: TestResponse = client.get("/static/js/index.js")

    assert response.status_code == HTTPStatus.OK
    # not asserting data here because the file content may change
