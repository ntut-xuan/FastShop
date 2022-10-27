from __future__ import annotations

import sqlite3
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from auth.util import (
    hash_with_sha512,
    is_registered,
    is_valid_birthday_format,
    is_valid_email,
)
from database import get_database

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


class TestRegisterRoute:
    @pytest.fixture
    def new_data(self) -> dict[str, str]:
        return {
            "e-mail": "abc@gmail.com",
            "password": "test",
            "firstname": "Huang",
            "lastname": "Han-Xuan",
            "sex": "0",
            "birthday": "2002-06-25",
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
                "SELECT * FROM user WHERE email = ?", ("abc@gmail.com",)
            ).fetchone()
            assert user_data["firstname"] == "Huang"
            assert user_data["lastname"] == "Han-Xuan"
            assert user_data["sex"] == 0
            # birthday and password are stored in different format,
            # not to bother with them here.

    def test_post_with_duplicate_data_should_be_forbidden(
        self, client: FlaskClient
    ) -> None:
        data: dict[str, str] = {
            "e-mail": "test@email.com",
            "password": "test",
            "firstname": "Huang",
            "lastname": "Han-Xuan",
            "sex": "0",
            "birthday": "2002-06-25",
        }

        resp: TestResponse = client.post("/register", json=data)

        assert resp.status_code == HTTPStatus.FORBIDDEN

    def test_post_with_wrong_data_should_be_bad_request(
        self, client: FlaskClient
    ) -> None:
        data: dict[str, str] = {"uriah": "garbage"}

        resp: TestResponse = client.post("/register", json=data)

        assert resp.status_code == HTTPStatus.BAD_REQUEST

    def test_post_with_wrong_date_format_should_be_unprocessable_entity(
        self, client: FlaskClient, new_data: dict[str, str]
    ) -> None:
        new_data["birthday"] = "2002/06/25"

        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_post_with_wrong_email_format_should_be_unprocessable_entity(
        self, client: FlaskClient, new_data: dict[str, str]
    ) -> None:
        new_data["e-mail"] = "test@email@com"

        resp: TestResponse = client.post("/register", json=new_data)

        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


class TestLoginRoute:
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

    def test_post_with_wrong_password_should_have_code_forbidden(
        self, client: FlaskClient
    ) -> None:
        email_and_password: dict[str, str] = {
            "e-mail": "test@email.com",
            "password": "should_be_test",
        }

        resp: TestResponse = client.post("/login", json=email_and_password)

        assert resp.status_code == HTTPStatus.FORBIDDEN

    def test_post_with_wrong_password_should_response_failed_message_in_json(
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


some_invalid_emails: list[str] = ["plainaddress", "#@%^%#$@#$@#.com", "@example.com", "Joe Smith <email@example.com>", "email.example.com", "email@example@example.com", ".email@example.com", "email..email@example.com", "email@example.com (Joe Smith)", "email@example", "email@-example.com", "email@111.222.333.44444", "email@example..com", "Abc..123@example.com"]  # fmt: skip
@pytest.mark.parametrize(
    argnames=("malform_email",),
    argvalues=(
        ("noletterafterdash-@email.com",),
        ("badsymbolindomain@ema#il.com",),
        ("multipleat@email@org.tw",),
        ("badsymbol#123@email.com",),
        (".startwithdot@email.com",),
        ("double..dot@email.com",),
        ("domainwithnodot@email",),
        ("missingat.email.com",),
        ("あいうえお@example.com",),
        *((invalid_email,) for invalid_email in some_invalid_emails),
    ),
)
def test_is_valid_email_on_malform_email_should_return_false(
    malform_email: str,
) -> None:
    assert not is_valid_email(malform_email)


@pytest.mark.parametrize(
    argnames=("email",),
    argvalues=(
        ("letterafterdash-123@email.com",),
        ("dot.in.middle@email.com",),
        ("under_score@email.com",),
        ("CAPTIAL@email.com",),
        ("123@email.com",),
    ),
)
def test_is_valid_email_on_valid_email_should_return_true(email: str) -> None:
    assert is_valid_email(email)


@pytest.mark.parametrize(
    argnames=("birthday_in_wrong_format",),
    argvalues=(
        ("2000/01/01",),
        ("2000_01_01",),
        ("01-01-2000",),
        ("2000.01.01",),
        ("20000101",),
    ),
)
def test_is_valid_birthday_format_on_wrong_format_should_return_false(
    birthday_in_wrong_format: str,
) -> None:
    assert not is_valid_birthday_format(birthday_in_wrong_format)


def test_is_valid_birthday_format_on_corret_format_should_return_true() -> None:
    birthday = "2000-01-01"

    assert is_valid_birthday_format(birthday)


@pytest.mark.parametrize(
    argnames=("bad_birthday",),
    argvalues=(
        ("2000/13/01",),  # bad month
        ("-1/01/01",),  # bad year
        ("2000/01/32",),  # bad day
    ),
)
def test_is_valid_birthday_format_on_bad_birthday_value_should_return_false(
    bad_birthday: str,
) -> None:
    assert not is_valid_birthday_format(bad_birthday)


def test_is_registered_on_registered_user_should_be_true(app: Flask) -> None:
    email: str = "test@email.com"
    password: str = "test"
    with app.app_context():

        assert is_registered(email, password)


def test_is_registered_on_unregistered_user_should_be_false(app: Flask) -> None:
    email: str = "unregistered@email.com"
    password: str = "unregistered"
    with app.app_context():

        assert not is_registered(email, password)
