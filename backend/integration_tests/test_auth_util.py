from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, ClassVar

import freezegun
import jwt
import pymysql
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
    fetch_user_profile,
    is_correct_password,
    is_registered,
    is_valid_birthday,
    is_valid_email,
    login,
    register,
)
from database import get_database

if TYPE_CHECKING:
    from flask import Flask


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
        assert not is_valid_birthday(birthday_in_incorrect_format)

    def test_on_correct_format_should_return_true(self) -> None:
        birthday = "2000-01-01"

        assert is_valid_birthday(birthday)

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
        assert not is_valid_birthday(bad_birthday)


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


class TestLogin:
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


class TestRegister:
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

            db: pymysql.Connection = get_database()  # type: ignore
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT `firstname`, `lastname`, `gender` FROM user WHERE email = %s",
                    (email,),
                )
                user_data: tuple = cursor.fetchone()

            assert user_data[0] == some_user_profile.firstname
            assert user_data[1] == some_user_profile.lastname
            assert user_data[2] == some_user_profile.gender


class TestFetchUserProfile:
    def test_with_unregister_email_should_rasie_exception(self, app: Flask) -> None:
        unregister_email = "c8763@ccc.nnn"
        with app.app_context():

            with pytest.raises(UserNotFoundError):
                fetch_user_profile(unregister_email)


class TestJWTCodec:
    @pytest.fixture
    def codec(self) -> JWTCodec:
        return JWTCodec(key="secret", algorithm="HS256")

    @freezegun.freeze_time("2000-01-01 00:00:00")
    def test_encode(self, codec: JWTCodec) -> None:
        data: dict[str, str] = {"some": "payload"}

        token: str = codec.encode(data, timedelta(days=1))

        expected: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNvbWUiOiJwYXlsb2FkIn0sImlhdCI6OTQ2Njg0ODAwLCJleHAiOjk0Njc3MTIwMH0.FU7fNuSrA-EuVtpE2duW-VD9hJX1B1QfPuQ2_kJ95Lw"
        assert token == expected

    def test_decode(self, codec: JWTCodec) -> None:
        token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg"

        data: dict = codec.decode(token)

        expected: dict[str, str] = {"some": "payload"}
        assert data == expected

    class TestIsValidJWT:
        def test_on_token_with_not_enough_segment_should_return_false(
            self,
            codec: JWTCodec,
        ) -> None:
            token: str = "should_have_three_dot_separated_segments"

            assert not codec.is_valid_jwt(token)

        def test_on_invalid_token_should_return_false(self, codec: JWTCodec) -> None:
            token: str = "this.failed.validation"

            assert not codec.is_valid_jwt(token)

        def test_on_expired_token_should_return_false(self, codec: JWTCodec) -> None:
            time_to_the_past = timedelta(days=-87)

            token: str = codec.encode({"some": "payload"}, time_to_the_past)

            assert not codec.is_valid_jwt(token)

        def test_on_vaild_token_should_return_true(self, codec: JWTCodec) -> None:
            payload: dict[str, str] = {"some": "payload"}
            token: str = jwt.encode(payload, key=codec.key, algorithm=codec.algorithm)

            is_valid_jwt: bool = codec.is_valid_jwt(token)

            assert is_valid_jwt
