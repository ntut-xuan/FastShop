from __future__ import annotations

from http import HTTPStatus
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

    @pytest.mark.parametrize(argnames="status_code", argvalues=(102, 226, 308))
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

    def test_should_map_no_param_rule_to_doc_path(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        expect_path = self.ExpectedDocPathFunctor("../api/test/some/rule/get.yml")
        monkeypatch.setattr("util.swag_from", expect_path)

        route_with_doc(Blueprint("test", __name__), "/some/rule", methods=["GET"])(
            self.dummy_func
        )

    def test_should_map_rule_with_params_to_doc_path(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        expect_path = self.ExpectedDocPathFunctor(
            "../api/test/some/param1/rule/param2/get.yml"
        )
        monkeypatch.setattr("util.swag_from", expect_path)

        route_with_doc(
            Blueprint("test", __name__), "/some/<param1>/rule/<param2>", methods=["GET"]
        )(self.dummy_func)

    def test_should_map_rule_with_typed_params_to_doc_path(
        self, monkeypatch: pytest.MonkeyPatch
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

    def test_should_map_rule_with_optionally_typed_params_to_doc_path(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        expect_path = self.ExpectedDocPathFunctor(
            "../api/test/some/has_type/rule/no_type/and/has_type/more/no_type/get.yml"
        )
        monkeypatch.setattr("util.swag_from", expect_path)

        route_with_doc(
            Blueprint("test", __name__),
            "/some/<int:has_type>/rule/<no_type>/and/<string:has_type>/more/<no_type>",
            methods=["GET"],
        )(self.dummy_func)

    class RulePassedToRouteShouldNotChangeFunctor:
        def __init__(self, expected_rule: str) -> None:
            self._expected_rule: str = expected_rule

        def __call__(self, actual_rule: str, *args, **kwargs):
            assert actual_rule == self._expected_rule

            def wrapper(func):
                return func

            return wrapper

    def test_rule_passed_to_bp_route_should_not_change(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        test_bp = Blueprint("test", __name__)
        rule = (
            "/some/<int:has_type>/rule/<no_type>/and/<string:has_type>/more/<no_type>"
        )
        # disable swag_from since it's irrelevant in this test
        monkeypatch.setattr("util.swag_from", lambda *x, **y: self.dummy_func)
        # monkeypatch route for the assertion
        test_bp.route = self.RulePassedToRouteShouldNotChangeFunctor(rule)  # type: ignore[assignment]

        route_with_doc(test_bp, rule, methods=["GET"])(self.dummy_func)
