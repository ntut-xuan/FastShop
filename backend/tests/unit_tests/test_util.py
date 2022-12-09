from __future__ import annotations

from http import HTTPStatus
import re
from typing import TYPE_CHECKING

import pytest
from flask import Blueprint

from util import SingleMessageStatus, fetch_page, route_with_doc

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


class TestRouteWithDocDecorator:
    def dummy_func(self, *args, **kwargs) -> None:
        """Dummy function as a wrappee. Left empty"""

    class ExpectedDocPathFunctor:
        def __init__(self, expected_path: str) -> None:
            self._expected_path = expected_path

        def __call__(self, doc_path: str, *args, **kwargs):
            assert doc_path == self._expected_path

            def wrapper(func):
                return func

            return wrapper

    def test_should_map_rule_to_doc_path(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        expect_path = self.ExpectedDocPathFunctor("../api/test/some/rule/get.yml")

        monkeypatch.setattr("util.swag_from", expect_path)

        route_with_doc(Blueprint("test", __name__), "/some/rule", methods=["GET"])(
            self.dummy_func
        )

    @pytest.mark.skip
    def test_should_map_rule_with_params_to_doc_path(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        expect_path = self.ExpectedDocPathFunctor(
            "../api/test/some/param1/rule/param2/get.yml"
        )

        monkeypatch.setattr("util.swag_from", expect_path)

        route_with_doc(
            Blueprint("test", __name__), "/some/<param1>/rule/<param2>", methods=["GET"]
        )(self.dummy_func)

    def test_should_map_rule_with_typed_params_to_doc_path(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        expect_path = self.ExpectedDocPathFunctor(
            "../api/test/some/param1/rule/param2/get.yml"
        )

        monkeypatch.setattr("util.swag_from", expect_path)

        route_with_doc(
            Blueprint("test", __name__),
            "/some/<int:param1>/rule/<string:param2>",
            methods=["GET"],
        )(self.dummy_func)


def test_regex_sub_should_remove_angle_bracket() -> None:
    pattern: re.Pattern = re.compile(r"<(.*?)>")
    string: str = "/some/<param1>/rule/<param2>"

    def remove_angle_bracket(m: re.Match) -> str:
        return m[0][1:-1]

    path = pattern.sub(remove_angle_bracket, string)
    assert path == "/some/param1/rule/param2"


def test_regex_sub_should_remove_angle_bracket_and_type() -> None:
    pattern: re.Pattern = re.compile(r"<(.*?)>")
    string: str = "/some/<int:param1>/rule/<string:param2>"

    def remove_angle_bracket_and_type(m: re.Match) -> str:
        match = re.findall(r"<.*:(.*?)>", m[0])
        return match[0]

    path = pattern.sub(remove_angle_bracket_and_type, string)
    assert path == "/some/param1/rule/param2"


def test_regex_sub_should_remove_angle_bracket_and_optional_type() -> None:
    pattern: re.Pattern = re.compile(r"<(.*?)>")
    string: str = "/some/<int:param1>/rule/<param2>"

    def remove_angle_bracket_and_type(m: re.Match) -> str:
        match = re.findall(r"<.*:(.*?)>", m[0])
        return match[0]

    path = pattern.sub(remove_angle_bracket_and_type, string)
    assert path == "/some/param1/rule/param2"
