from __future__ import annotations

import sqlite3
from datetime import timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING, ClassVar, no_type_check

import pytest

from auth.exception import (
    EmailAlreadyRegisteredError,
    IncorrectEmailOrPasswordError,
    UserNotFoundError,
)
from auth.util import (
    Gender,
    JWTCodec,
    UserProfile,
    decode_jwt,
    fetch_specific_account_profile,
    generate_payload,
    is_correct_password,
    is_registered,
    is_valid_birthday_format,
    is_valid_email,
    is_valid_jwt_data,
    login,
    register,
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

        assert cookie != None
        assert is_valid_jwt_data(str(cookie.value)) == True

    @no_type_check
    def test_post_with_correct_data_should_have_correct_jwt_token_attribute(
        self,
        client: FlaskClient,
        new_data: dict[str, str],
    ) -> None:
        client.post("/login", json=new_data)
        cookie = next(
            (cookie for cookie in client.cookie_jar if cookie.name == "jwt"), None
        )
        cookie_value = str(cookie.value)
        jwt_data = decode_jwt(cookie_value)

        assert jwt_data["data"]["e-mail"] == new_data["e-mail"]
        assert jwt_data["data"]["firstname"] == new_data["firstname"]
        assert jwt_data["data"]["lastname"] == new_data["lastname"]
        assert jwt_data["data"]["gender"] == new_data["gender"]


class TestIsValidEmail:
    _some_invalid_emails: ClassVar[list[str]] = ["plainaddress", "#@%^%#$@#$@#.com", "@example.com", "Joe Smith <email@example.com>", "email.example.com", "email@example@example.com", ".email@example.com", "email..email@example.com", "email@example.com (Joe Smith)", "email@example", "email@-example.com", "email@111.222.333.44444", "email@example..com", "Abc..123@example.com"]  # fmt: skip
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
            *((invalid_email,) for invalid_email in _some_invalid_emails),
        ),
    )
    def test_on_malform_email_should_return_false(self, malform_email: str) -> None:
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
    def test_on_valid_email_should_return_true(self, email: str) -> None:
        assert is_valid_email(email)


class TestIsValidBirthday:
    @pytest.mark.parametrize(
        argnames=("birthday_in_incorrect_format",),
        argvalues=(
            ("2000/01/01",),
            ("2000_01_01",),
            ("01-01-2000",),
            ("2000.01.01",),
            ("20000101",),
        ),
    )
    def test_on_incorrect_format_should_return_false(
        self,
        birthday_in_incorrect_format: str,
    ) -> None:
        assert not is_valid_birthday_format(birthday_in_incorrect_format)

    def test_on_correct_format_should_return_true(self) -> None:
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
    def test_on_bad_birthday_value_should_return_false(
        self,
        bad_birthday: str,
    ) -> None:
        assert not is_valid_birthday_format(bad_birthday)


class TestIsCorrectPassword:
    def test_on_correct_password_should_be_true(self, app: Flask) -> None:
        email: str = "test@email.com"
        password: str = "test"
        with app.app_context():

            assert is_correct_password(email, password)

    def test_on_incorrect_user_should_be_false(self, app: Flask) -> None:
        email: str = "test@email.com"
        password: str = "should_be_test"
        with app.app_context():

            assert not is_correct_password(email, password)

    def test_on_unregistered_email_should_raise_exception(self, app: Flask) -> None:
        email: str = "unregistered@email.com"
        password: str = "test"
        with app.app_context():

            with pytest.raises(Exception):
                is_correct_password(email, password)


class TestIsRegistered:
    def test_on_registered_email_should_be_true(self, app: Flask) -> None:
        registered_email: str = "test@email.com"
        with app.app_context():

            assert is_registered(registered_email)

    def test_on_unregistered_email_should_be_false(self, app: Flask) -> None:
        unregistered_email: str = "unregistered@email.com"
        with app.app_context():

            assert not is_registered(unregistered_email)


class TestLoginFunction:
    def test_on_unregistered_email_should_raise_exception(self, app: Flask) -> None:
        unregistered_email: str = "unregistered@email.com"
        password: str = "test"
        with app.app_context():

            with pytest.raises(IncorrectEmailOrPasswordError):
                login(unregistered_email, password)

    def test_on_incorrect_password_should_raise_exception(self, app: Flask) -> None:
        email: str = "test@email.com"
        incorrect_password: str = "should_be_test"
        with app.app_context():

            with pytest.raises(IncorrectEmailOrPasswordError):
                login(email, incorrect_password)


class TestRegisterFunction:
    @pytest.fixture
    def some_user_profile(self) -> UserProfile:
        return UserProfile("Han-Xuan", "Huang", Gender.MALE, 1666604387)

    def test_on_registered_email_should_raise_exception(
        self, app: Flask, some_user_profile: UserProfile
    ) -> None:
        email: str = "test@email.com"
        password: str = "no_matter_the_password_is_registered_or_not"
        with app.app_context():

            with pytest.raises(EmailAlreadyRegisteredError):
                register(email, password, some_user_profile)

    def test_on_registered_password_should_registered_successfully(
        self, app: Flask, some_user_profile: UserProfile
    ) -> None:
        email: str = "unregistered_email@email.com"
        password: str = "test"
        with app.app_context():

            register(email, password, some_user_profile)

            db: sqlite3.Connection = get_database()  # type: ignore
            db.row_factory = sqlite3.Row
            user_data: sqlite3.Row = db.execute(
                "SELECT * FROM user WHERE email = ?", (email,)
            ).fetchone()
            assert user_data["firstname"] == some_user_profile.firstname
            assert user_data["lastname"] == some_user_profile.lastname
            assert user_data["gender"] == some_user_profile.gender


class TestFetchProfileFunction:
    def test_with_unregister_email_should_rasie_exception(self, app: Flask) -> None:
        unregister_email = "c8763@ccc.nnn"
        with app.app_context():

            with pytest.raises(UserNotFoundError):

                fetch_specific_account_profile(unregister_email)


class TestIsValidJWTData:
    def test_on_data_with_not_enought_segment_should_return_false(
        self,
    ) -> None:
        some_jwt_key = "abc123"
        assert not is_valid_jwt_data(some_jwt_key)

    def test_on_invalid_data_should_return_false(self) -> None:
        some_jwt_key = "abc.123.bcd"
        assert not is_valid_jwt_data(some_jwt_key)

    def test_on_expired_data_should_return_false(self) -> None:
        expired_jwt_payload = generate_payload({}, timedelta(days=-87))
        assert not is_valid_jwt_data(expired_jwt_payload)


class TestJWTCodec:
    def test_encode(self) -> None:
        data: dict[str, str] = {"some": "payload"}
        codec = JWTCodec(key="secret", algorithm="HS256")

        token: str = codec.encode(data)

        expected: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg"
        assert token == expected

    def test_decode(self) -> None:
        token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg"
        codec = JWTCodec(key="secret", algorithm="HS256")

        data: dict = codec.decode(token)

        expected: dict[str, str] = {"some": "payload"}
        assert data == expected
