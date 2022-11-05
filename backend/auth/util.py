import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import IntEnum
from typing import Any, Final

import jwt
from flask import current_app

from auth.exception import (
    EmailAlreadyRegisteredError,
    IncorrectEmailOrPasswordError,
    UserNotFoundError,
)
from database.util import execute_command

EMAIL_REGEX: Final[str] = r"^[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*@[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*(\.[A-Za-z0-9_]{2,3})+$"  # fmt: skip
BIRTHDAY_FORMAT: Final[str] = "%Y-%m-%d"


def is_fullmatched_with_regex(string: str, regex: str) -> bool:
    return bool(re.fullmatch(regex, string))


def is_valid_email(email: str) -> bool:
    return is_fullmatched_with_regex(email, EMAIL_REGEX)


def is_valid_birthday(birthday: str) -> bool:
    """Returns whether `birthday` is in format "%Y-%m-%d" and the day exists."""
    try:
        datetime.strptime(birthday, BIRTHDAY_FORMAT)
        return True
    except ValueError:
        return False


def login(email: str, password: str) -> None:
    """
    Raises:
        IncorrectEmailOrPasswordError
    """
    if not is_registered(email) or not is_correct_password(email, password):
        raise IncorrectEmailOrPasswordError
    # TODO: modify some cookie to mark the user as logged in


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


class JWTCodec:
    def __init__(self, key: str = "secret", algorithm: str = "HS256") -> None:
        self._key: str = key
        self._algorithm: str = algorithm

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
            return True
        except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
            return False


def register(email: str, password: str, profile: UserProfile) -> None:
    """
    Raises:
        EmailAlreadyRegisteredError: `email` should not be already registered.
    """

    if is_registered(email):
        raise EmailAlreadyRegisteredError

    if current_app.config["TESTING"] is True:
        stmt_to_insert_new_user: str = """
            INSERT INTO `user`(`email`, `password`, `firstname`, `lastname`, `gender`, `birthday`)
                VALUES(?, ?, ?, ?, ?, ?)
        """
    else:
        stmt_to_insert_new_user = """
            INSERT INTO `user`(`email`, `password`, `firstname`, `lastname`, `gender`, `birthday`)
                VALUES(%s, %s, %s, %s, %s, %s)
        """

    execute_command(
        stmt_to_insert_new_user,
        (
            email,
            hash_with_sha512(password),
            profile.firstname,
            profile.lastname,
            int(profile.gender),
            profile.birthday,
        ),
    )


def is_correct_password(registered_email: str, password_to_check: str) -> bool:
    """The `registered_email` should be already registered, otherwise Exception raised by the database."""

    if current_app.config["TESTING"] is True:
        database_execute_command = "SELECT `password` FROM `user` WHERE `email` = ?"
    else:
        database_execute_command = "SELECT `password` FROM `user` WHERE `email` = %s"

    hashed_password_to_check = hash_with_sha512(password_to_check)
    hashed_user_password: int = execute_command(
        database_execute_command,
        (registered_email,),
    )[0]["password"]

    return hashed_password_to_check == hashed_user_password


def is_registered(email: str) -> bool:
    """Returns whether the email is aldready used."""

    if current_app.config["TESTING"] is True:
        database_execute_command = (
            "SELECT COUNT(*) as `user_count` FROM `user` WHERE `email` = ?"
        )
    else:
        database_execute_command = (
            "SELECT COUNT(*) as `user_count` FROM `user` WHERE `email` = %s"
        )

    user_count: int = execute_command(database_execute_command, (email,),)[
        0
    ]["user_count"]

    return user_count != 0


def hash_with_sha512(string: str) -> str:
    return hashlib.sha512(string.encode("utf-8")).hexdigest()


def fetch_user_profile(email: str) -> dict[str, Any]:
    """
    Raises:
        UserNotFoundError: No registered user with email `email`.
    """

    if current_app.config["TESTING"] is True:
        database_execute_command = "SELECT `firstname`, `lastname`, `gender`, `birthday` FROM `user` WHERE `email` = ?"
    else:
        database_execute_command = "SELECT `firstname`, `lastname`, `gender`, `birthday` FROM `user` WHERE `email` = %s"

    if not is_registered(email):
        raise UserNotFoundError

    return execute_command(
        database_execute_command,
        (email,),
    )[0]
