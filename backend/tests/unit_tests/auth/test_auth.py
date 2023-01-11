from __future__ import annotations

from http import HTTPStatus
from http.cookiejar import Cookie, CookieJar
from typing import TYPE_CHECKING, Any

import pytest

from src.auth.util import Gender, HS256JWTCodec
from src.database import db
from src.models import User
from tests.util import assert_not_raise

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from sqlalchemy.engine.row import Row
    from sqlalchemy.sql.selectable import Select
    from werkzeug.test import TestResponse


class TestRegisterRoute:
    @pytest.fixture
    def new_data(self) -> dict[str, Any]:
        return {
            "e-mail": "new@gmail.com",
            "password": "abc",
            "firstname": "new_firstname",
            "lastname": "new_lastname",
            "gender": 1,
            "birthday": "2001-01-01",
        }

    def test_get_should_response_content_of_register_html(
        self, client: FlaskClient
    ) -> None:
        resp: TestResponse = client.get("/register")

        assert b"<!-- register.html (a marker for API test) -->" in resp.data

    def test_post_with_correct_data_should_have_code_ok(
        self, client: FlaskClient, new_data: dict[str, Any]
    ) -> None:
        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.OK

    def test_post_with_correct_data_should_store_into_database(
        self, client: FlaskClient, new_data: dict[str, Any]
    ) -> None:
        with client.application.app_context():

            client.post("/register", json=new_data)

        with client.application.app_context():
            stmt: Select = db.select(User.firstname, User.lastname, User.gender).where(
                User.email == "new@gmail.com"
            )
            user: Row = db.session.execute(stmt).fetchone()
            assert user.firstname == "new_firstname"
            assert user.lastname == "new_lastname"
            assert user.gender == Gender.FEMALE
            # birthday and password are stored in different format,
            # not to bother with them here.

    def test_post_with_registered_data_should_be_forbidden(
        self, client: FlaskClient
    ) -> None:
        data: dict[str, Any] = {
            "e-mail": "test@email.com",
            "password": "test",
            "firstname": "Han-Xuan",
            "lastname": "Huang",
            "gender": 0,
            "birthday": "2002-06-25",
        }

        resp: TestResponse = client.post("/register", json=data)

        assert resp.status_code == HTTPStatus.FORBIDDEN

    def test_post_with_incorrect_data_should_be_bad_request(
        self, client: FlaskClient
    ) -> None:
        data: dict[str, str] = {"uriah": "garbage"}

        resp: TestResponse = client.post("/register", json=data)

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_post_with_incorrect_date_format_should_be_unprocessable_entity(
        self, client: FlaskClient, new_data: dict[str, Any]
    ) -> None:
        new_data["birthday"] = "2001/01/01"

        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_post_with_incorrect_email_format_should_be_unprocessable_entity(
        self, client: FlaskClient, new_data: dict[str, Any]
    ) -> None:
        new_data["e-mail"] = "test@email@com"

        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestLoginRoute:
    @pytest.fixture
    def new_data(self) -> dict[str, Any]:
        return {
            "e-mail": "test@email.com",
            "password": "test",
            "firstname": "Han-Xuan",
            "lastname": "Huang",
            "gender": 0,
            "birthday": "2002-06-25",
        }

    def test_get_should_response_content_of_login_html(
        self, client: FlaskClient
    ) -> None:
        resp: TestResponse = client.get("/login")

        assert b"<!-- login.html (a marker for API test) -->" in resp.data

    def test_post_with_existing_email_and_password_should_have_code_ok(
        self, client: FlaskClient
    ) -> None:
        email_and_password: dict[str, str] = {
            "e-mail": "test@email.com",
            "password": "test",
        }

        resp: TestResponse = client.post("/login", json=email_and_password)

        assert resp.status_code == HTTPStatus.OK

    def test_post_with_incorrect_password_should_have_code_forbidden(
        self, client: FlaskClient
    ) -> None:
        email_and_password: dict[str, str] = {
            "e-mail": "test@email.com",
            "password": "should_be_test",
        }

        resp: TestResponse = client.post("/login", json=email_and_password)

        assert resp.status_code == HTTPStatus.FORBIDDEN

    def test_post_with_incorrect_password_should_response_failed_message_in_json(
        self, client: FlaskClient
    ) -> None:
        email_and_password: dict[str, str] = {
            "e-mail": "test@email.com",
            "password": "should_be_test",
        }

        resp: TestResponse = client.post("/login", json=email_and_password)

        assert resp.is_json
        assert (
            resp.json is not None
            and resp.json["message"]
            == "The email or password that the user posted does not match any account."
        )

    def test_post_with_invalid_data_should_have_code_bad_request(
        self, client: FlaskClient
    ) -> None:
        invalid_data: dict[str, str] = {"uriah": "garbage"}

        resp: TestResponse = client.post("/login", json=invalid_data)

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_post_with_invalid_data_should_response_failed_message_in_json(
        self, client: FlaskClient
    ) -> None:
        invalid_data: dict[str, str] = {"uriah": "garbage"}

        resp: TestResponse = client.post("/login", json=invalid_data)

        assert resp.is_json
        assert (
            resp.json is not None
            and resp.json["message"]
            == "The data has the wrong format and the server can't understand it."
        )

    def test_post_with_invalid_email_should_have_code_unprocessable_entity(
        self, client: FlaskClient
    ) -> None:
        invalid_email: str = "t109590031@ntut@org@tw"
        data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

        resp: TestResponse = client.post("/login", json=data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_post_with_invalid_email_should_response_failed_message_in_json(
        self, client: FlaskClient
    ) -> None:
        invalid_email: str = "t109590031@ntut@org@tw"
        data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

        resp: TestResponse = client.post("/login", json=data)

        assert resp.is_json
        assert (
            resp.json is not None
            and resp.json["message"]
            == "The posted data has the correct format, but the data is invalid."
        )

    def test_post_with_existing_email_and_password_should_exist_jwt_cookie(
        self, client: FlaskClient, new_data: dict[str, Any]
    ) -> None:
        client.post("/login", json=new_data)

        cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
        with assert_not_raise(ValueError):
            (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))

    def test_post_with_correct_data_should_have_correct_jwt_token_attribute(
        self, app: Flask, client: FlaskClient, new_data: dict[str, Any]
    ) -> None:
        codec = HS256JWTCodec(app.config["jwt_key"])

        client.post("/login", json=new_data)

        cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
        (jwt_cookie,) = tuple(filter(lambda x: x.name == "jwt", cookies))
        assert jwt_cookie.value is not None
        jwt_payload: dict[str, Any] = codec.decode(jwt_cookie.value)
        data = jwt_payload["data"]
        assert data["e-mail"] == new_data["e-mail"]
        assert data["firstname"] == new_data["firstname"]
        assert data["lastname"] == new_data["lastname"]
        assert data["gender"] == new_data["gender"]


class TestVerifyJWT:
    @pytest.fixture
    def payload(self) -> dict[str, Any]:
        return {
            "e-mail": "test@email.com",
            "password": "test",
            "firstname": "Han-Xuan",
            "lastname": "Huang",
            "gender": 0,
            "birthday": "2002-06-25",
        }

    def test_post_with_valid_jwt_cookie_should_have_code_http_ok(
        self, app: Flask, client: FlaskClient, payload: dict[str, Any]
    ) -> None:
        jwt_token: str = HS256JWTCodec(app.config["jwt_key"]).encode(payload)
        client.set_cookie("localhost", "jwt", jwt_token)

        resp: TestResponse = client.post("/verify_jwt")

        assert resp.status_code == HTTPStatus.OK

    def test_post_with_valid_jwt_cookie_should_return_payload_in_json(
        self, app: Flask, client: FlaskClient, payload: dict[str, Any]
    ) -> None:
        jwt_token: str = HS256JWTCodec(app.config["jwt_key"]).encode(payload)
        client.set_cookie("localhost", "jwt", jwt_token)

        resp: TestResponse = client.post("/verify_jwt")

        assert resp.is_json
        assert resp.json["data"] == payload  # type: ignore[index]

    def test_post_with_absent_jwt_cookie_should_have_code_http_unauthorized(
        self, client: FlaskClient
    ) -> None:
        resp: TestResponse = client.post("/verify_jwt")

        assert resp.status_code == HTTPStatus.UNAUTHORIZED

    def test_post_with_absent_jwt_cookie_should_return_failed_message_in_json(
        self, client: FlaskClient
    ) -> None:
        resp: TestResponse = client.post("/verify_jwt")

        assert resp.is_json
        assert (
            resp.json["message"]  # type: ignore[index]
            == "The specific cookie does not exist in the request header."
        )

    def test_post_with_invalid_jwt_cookie_should_have_code_http_unprocessable_entity(
        self, client: FlaskClient
    ) -> None:
        client.set_cookie("localhost", "jwt", "aaa.bbb.ccc")

        resp: TestResponse = client.post("/verify_jwt")

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_post_with_invalid_jwt_cookie_should_return_failed_message_in_json(
        self, client: FlaskClient
    ) -> None:
        client.set_cookie("localhost", "jwt", "aaa.bbb.ccc")

        resp: TestResponse = client.post("/verify_jwt")

        assert resp.is_json
        assert (
            resp.json["message"]  # type: ignore[index]
            == "The specific cookie in the request header is invalid."
        )


class TestLogoutRoute:
    def test_if_jwt_exist_should_return_ok(self, client: FlaskClient) -> None:
        client.set_cookie("localhost", "jwt", "aaa.bbb.ccc")

        resp: TestResponse = client.post("/logout")

        assert resp.status_code == HTTPStatus.OK

    def test_if_jwt_exist_should_let_jwt_token_absent(
        self, client: FlaskClient
    ) -> None:
        client.set_cookie("localhost", "jwt", "aaa.bbb.ccc")

        client.post("/logout")

        cookies: tuple[Cookie, ...] = _get_cookies(client.cookie_jar)
        assert not cookies

    def test_if_jwt_absent_should_return_ok(self, client: FlaskClient) -> None:
        resp: TestResponse = client.post("/logout")

        assert resp.status_code == HTTPStatus.OK


def _get_cookies(cookie_jar: CookieJar | None) -> tuple[Cookie, ...]:
    if cookie_jar is None:
        return tuple()
    return tuple(cookie for cookie in cookie_jar)
