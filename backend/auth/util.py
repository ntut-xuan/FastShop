import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import IntEnum
from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Final

import jwt
from flask import current_app, make_response, redirect, request
from sqlalchemy import select

from auth.exception import EmailAlreadyRegisteredError, UserNotFoundError
from database import db
from models import User
from util import SingleMessageStatus

if TYPE_CHECKING:
    from sqlalchemy.engine.row import Row
    from sqlalchemy.sql.dml import Insert
    from sqlalchemy.sql.selectable import Select

EMAIL_REGEX: Final[str] = r"^[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*@[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*(\.[A-Za-z0-9_]{2,3})+$"  # fmt: skip
BIRTHDAY_FORMAT: Final[str] = "%Y-%m-%d"


def is_full_matched_with_regex(string: str, regex: str) -> bool:
    return bool(re.fullmatch(regex, string))


def is_valid_email(email: str) -> bool:
    return is_full_matched_with_regex(email, EMAIL_REGEX)


def is_valid_birthday(birthday: str) -> bool:
    """Returns whether `birthday` is in format "%Y-%m-%d" and the day exists."""
    try:
        datetime.strptime(birthday, BIRTHDAY_FORMAT)
    except ValueError:
        return False
    return True


@dataclass
class Gender(IntEnum):
    MALE = 0
    FEMALE = 1


@dataclass
class UserProfile:
    firstname: str
    lastname: str
    gender: Gender
    birthday: int


class HS256JWTCodec:
    def __init__(self, key: str) -> None:
        self._key: Final[str] = key
        self._algorithm: Final[str] = "HS256"

    @property
    def key(self) -> str:
        return self._key

    @property
    def algorithm(self) -> str:
        return self._algorithm

    def encode(
        self,
        payload: dict[str, Any],
        expiration_time_delta: timedelta = timedelta(days=1),
    ) -> str:
        """Returns the JWT with `data`, Issue At (iat) and Expiration Time (exp) as payload."""
        current_time: datetime = datetime.now(tz=timezone.utc)
        expiration_time: datetime = current_time + expiration_time_delta
        payload = {
            "data": payload,
            "iat": current_time,
            "exp": expiration_time,
        }
        token: str = jwt.encode(payload, key=self._key, algorithm=self._algorithm)
        return token

    def decode(self, token: str) -> dict[str, Any]:
        data: dict[str, Any] = jwt.decode(
            token, key=self._key, algorithms=[self._algorithm]
        )
        return data

    def is_valid_jwt(self, token: str) -> bool:
        """Returns False if the expiration time (exp) is in the past or it failed validation."""
        try:
            self.decode(token)
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False
        return True


def register(email: str, password: str, profile: UserProfile) -> None:
    """
    Raises:
        EmailAlreadyRegisteredError: `email` should not be already registered.
    """

    if is_registered(email):
        raise EmailAlreadyRegisteredError(email)

    insert_new_user_stmt: Insert = db.insert(User).values(
        email=email,
        password=hash_with_sha512(password),
        firstname=profile.firstname,
        lastname=profile.lastname,
        gender=profile.gender,
        birthday=profile.birthday,
    )
    db.session.execute(insert_new_user_stmt)
    db.session.commit()


def is_correct_password(registered_email: str, password_to_check: str) -> bool:
    """The `registered_email` should be already registered, otherwise Exception raised by the database."""
    select_password_with_email_stmt: Select = db.select(User.password).where(
        User.email == registered_email
    )
    password: str = db.session.execute(select_password_with_email_stmt).scalar_one()

    return hash_with_sha512(password_to_check) == password


def is_registered(email: str) -> bool:
    """Returns whether the email is already used."""
    select_user_with_email_stmt: Select = db.select(User).where(User.email == email)

    user_count: int = len(db.session.execute(select_user_with_email_stmt).all())
    return user_count != 0


def hash_with_sha512(string: str) -> str:
    return hashlib.sha512(string.encode("utf-8")).hexdigest()


def fetch_user_profile(email: str) -> dict[str, Any]:
    """
    Raises:
        UserNotFoundError: No registered user with email `email`.
    """
    if not is_registered(email):
        raise UserNotFoundError

    select_user_profile_with_email_stmt: Select = select(
        User.firstname, User.lastname, User.gender, User.birthday
    ).where(User.email == email)
    user_profile: Row = db.session.execute(
        select_user_profile_with_email_stmt
    ).fetchone()
    return dict(user_profile)


def verify_login_or_return_401(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        codec = HS256JWTCodec(current_app.config["jwt_key"])
        cookie: str | None = request.cookies.get("jwt")

        if cookie is None or not codec.is_valid_jwt(cookie):
            status = SingleMessageStatus(HTTPStatus.UNAUTHORIZED, "Unauthorized.")
            return make_response(status.message, status.code)

        return func(*args, **kwargs)

    return wrapper


def verify_login_or_redirect_login_page(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        codec = HS256JWTCodec(current_app.config["jwt_key"])
        cookie: str | None = request.cookies.get("jwt")

        if cookie is None or not codec.is_valid_jwt(cookie):
            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper
