from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

from auth.util import validate_email

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


def test_get_register_should_response_content_of_register_html(
    client: FlaskClient,
) -> None:
    resp: TestResponse = client.get("/register")

    assert b"<!-- register.html (a marker for API test) -->" in resp.data


def test_get_login_should_response_content_of_login_html(client: FlaskClient) -> None:
    resp: TestResponse = client.get("/login")

    assert b"<!-- login.html (a marker for API test) -->" in resp.data


def test_post_login_with_invalid_data_should_have_code_bad_request(
    client: FlaskClient,
) -> None:
    invalid_data: dict[str, str] = {"uriah": "garbage"}

    resp: TestResponse = client.post("/login", json=invalid_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_post_login_with_invalid_data_should_response_failed_message_in_json(
    client: FlaskClient,
) -> None:
    invalid_data: dict[str, str] = {"uriah": "garbage"}

    resp: TestResponse = client.post("/login", json=invalid_data)

    assert resp.is_json
    assert resp.json is not None and resp.json["status"] == "Failed"


def test_post_login_with_invalid_email_should_have_code_unprocessable_entity(
    client: FlaskClient,
) -> None:
    invalid_email: str = "t109590031@ntut@org@tw"
    data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

    resp: TestResponse = client.post("/login", json=data)

    assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_post_login_with_invalid_email_should_response_failed_message_in_json(
    client: FlaskClient,
) -> None:
    invalid_email: str = "t109590031@ntut@org@tw"
    data: dict[str, str] = {"e-mail": invalid_email, "password": "12345678"}

    resp: TestResponse = client.post("/login", json=data)

    assert resp.is_json
    assert resp.json is not None and resp.json["status"] == "Failed"


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
def test_validate_email_on_malform_email_should_return_false(
    malform_email: str,
) -> None:
    assert not validate_email(malform_email)


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
def test_validate_email_on_valid_email_should_return_true(email: str) -> None:
    assert validate_email(email)
