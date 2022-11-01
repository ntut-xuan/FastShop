from __future__ import annotations

import sqlite3
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, no_type_check

import pytest

from auth.util import Gender, JWTCodec
from database import get_database

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


class TestRegisterRoute:
    @pytest.fixture
    def new_data(self) -> dict[str, str]:
        return {
            "e-mail": "new@gmail.com",
            "password": "abc",
            "firstname": "new_firstname",
            "lastname": "new_lastname",
            "gender": "1",
            "birthday": "2001-01-01",
        }

    def test_get_should_response_content_of_register_html(
        self, client: FlaskClient
    ) -> None:
        resp: TestResponse = client.get("/register")

        assert b"<!-- register.html (a marker for API test) -->" in resp.data

    def test_post_with_correct_data_should_have_code_ok(
        self, client: FlaskClient, new_data: dict[str, str]
    ) -> None:
        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.OK

    def test_post_with_correct_data_should_store_into_database(
        self, client: FlaskClient, new_data: dict[str, str]
    ) -> None:
        with client.application.app_context():
            db: sqlite3.Connection = get_database()  # type: ignore
            db.row_factory = sqlite3.Row

            client.post("/register", json=new_data)

            user_data: sqlite3.Row = db.execute(
                "SELECT * FROM user WHERE email = ?", ("new@gmail.com",)
            ).fetchone()
            assert user_data["firstname"] == "new_firstname"
            assert user_data["lastname"] == "new_lastname"
            assert user_data["gender"] == Gender.FEMALE
            # birthday and password are stored in different format,
            # not to bother with them here.

    def test_post_with_registered_data_should_be_forbidden(
        self, client: FlaskClient
    ) -> None:
        data: dict[str, str] = {
            "e-mail": "test@email.com",
            "password": "test",
            "firstname": "Han-Xuan",
            "lastname": "Huang",
            "gender": "0",
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
        self, client: FlaskClient, new_data: dict[str, str]
    ) -> None:
        new_data["birthday"] = "2001/01/01"

        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_post_with_incorrect_email_format_should_be_unprocessable_entity(
        self, client: FlaskClient, new_data: dict[str, str]
    ) -> None:
        new_data["e-mail"] = "test@email@com"

        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestLoginRoute:
    @pytest.fixture
    def new_data(self) -> dict[str, str | int]:
        return {
            "e-mail": "test@email.com",
            "password": "test",
            "firstname": "Han-Xuan",
            "lastname": "Huang",
            "gender": 0,
            "birthday": "2002-06-25",
        }

    def test_get_should_response_content_of_login_html(
        self,
        client: FlaskClient,
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
        assert resp.json is not None and resp.json["message"] == "Failed"

    def test_post_with_invalid_data_should_have_code_bad_request(
        self,
        client: FlaskClient,
    ) -> None:
        invalid_data: dict[str, str] = {"uriah": "garbage"}

        resp: TestResponse = client.post("/login", json=invalid_data)

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_post_with_invalid_data_should_response_failed_message_in_json(
        self,
        client: FlaskClient,
    ) -> None:
        invalid_data: dict[str, str] = {"uriah": "garbage"}

        resp: TestResponse = client.post("/login", json=invalid_data)

        assert resp.is_json
        assert resp.json is not None and resp.json["message"] == "Failed"

    def test_post_with_invalid_email_should_have_code_unprocessable_entity(
        self,
        client: FlaskClient,
    ) -> None:
        invalid_email: str = "t109590031@ntut@org@tw"
        data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

        resp: TestResponse = client.post("/login", json=data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_post_with_invalid_email_should_response_failed_message_in_json(
        self,
        client: FlaskClient,
    ) -> None:
        invalid_email: str = "t109590031@ntut@org@tw"
        data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

        resp: TestResponse = client.post("/login", json=data)

        assert resp.is_json
        assert resp.json is not None and resp.json["message"] == "Failed"

    @no_type_check
    def test_post_with_existing_email_and_password_should_exist_jwt_cookie(
        self,
        client: FlaskClient,
        new_data: dict[str, str | int],
    ) -> None:
        client.post("/login", json=new_data)
        cookie = next(
            (cookie for cookie in client.cookie_jar if cookie.name == "jwt"), None
        )

        assert cookie is not None

    @no_type_check
    def test_post_with_correct_data_should_have_correct_jwt_token_attribute(
        self,
        client: FlaskClient,
        new_data: dict[str, str],
    ) -> None:
        codec = JWTCodec()

        client.post("/login", json=new_data)

        cookie = next(
            (cookie for cookie in client.cookie_jar if cookie.name == "jwt"), None
        )
        jwt_payload: dict[str, Any] = codec.decode(str(cookie.value))
        data = jwt_payload["data"]
        assert data["e-mail"] == new_data["e-mail"]
        assert data["firstname"] == new_data["firstname"]
        assert data["lastname"] == new_data["lastname"]
        assert data["gender"] == new_data["gender"]
