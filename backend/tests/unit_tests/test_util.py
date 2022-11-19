from __future__ import annotations

import pytest
from http import HTTPStatus
from typing import TYPE_CHECKING

from util import SingleMessageStatus, fetch_page

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_fetch_page(client: FlaskClient) -> None:
    with client.application.app_context():
        page_content: str = fetch_page("index")

    assert "index.html (a marker for API test)" in page_content


def test_get_static_file_should_have_code_ok(client: FlaskClient) -> None:
    response: TestResponse = client.get("/static/js/index.js")

    assert response.status_code == HTTPStatus.OK
    # not asserting data here because the file content may change


class TestSingleMessageStatus:
    def test_message_wrapped_as_dict(self) -> None:
        status = SingleMessageStatus(HTTPStatus.OK, "page returned")

        assert status.message == {"message": "page returned"}

    @pytest.mark.parametrize(
        argnames=("status_code",), argvalues=((102,), (226,), (308,))
    )
    def test_default_message_on_not_error_status_code_should_be_ok(
        self, status_code: int
    ) -> None:
        status = SingleMessageStatus(status_code)

        assert status.message["message"] == "OK"
