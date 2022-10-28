import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import Final

from database.util import execute_command

EMAIL_REGEX: Final[str] = r"^[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*@[A-Za-z0-9_]+([.-]?[A-Za-z0-9_]+)*(\.[A-Za-z0-9_]{2,3})+$"  # fmt: skip
BIRTHDAY_FORMAT: Final[str] = "%Y-%m-%d"


def is_fullmatched_with_regex(string: str, regex: str) -> bool:
    return bool(re.fullmatch(regex, string))


def is_valid_email(email: str) -> bool:
    return is_fullmatched_with_regex(email, EMAIL_REGEX)


def is_valid_birthday_format(birthday: str) -> bool:
    try:
        datetime.strptime(birthday, BIRTHDAY_FORMAT)
        return True
    except ValueError:
        return False


class UserUnregisteredError(RuntimeError):
    pass


def login(email: str, password: str) -> None:
    """
    Raises:
        UserUnregisteredError
    """
    if not is_registered(email, password):
        raise UserUnregisteredError
    # TODO: modify some cookie to mark the user as logged in


@dataclass
class Sex(IntEnum):
    MALE = 0
    FEMALE = 1


@dataclass
class UserProfile:
    firstname: str
    lastname: str
    sex: Sex
    birthday: int


class UserAlreadyRegisteredError(RuntimeError):
    pass


def register(email: str, password: str, profile: UserProfile) -> None:
    """
    Raises:
        UserAlreadyRegisteredError
    """
    hashed_password: str = hash_with_sha512(password)

    if is_registered(email, hashed_password, is_hashed=True):
        raise UserAlreadyRegisteredError

    stmt_to_insert_new_user: str = "INSERT INTO `user`(`email`, `password`, `firstname`, `lastname`, `sex`, `birthday`) VALUES(?, ?, ?, ?, ?, ?)"
    execute_command(
        stmt_to_insert_new_user,
        (
            email,
            hashed_password,
            profile.firstname,
            profile.lastname,
            profile.sex,
            profile.birthday,
        ),
    )


def is_registered(email: str, password: str, is_hashed: bool = False) -> bool:
    if not is_hashed:
        password = hash_with_sha512(password)
    user_count: int = execute_command(
        "SELECT COUNT(*) as `user_count` FROM `user` WHERE `email` = ? and `password` = ?",
        (email, password),
    )[0]["user_count"]

    return user_count != 0


def hash_with_sha512(string: str) -> str:
    return hashlib.sha512(string.encode("utf-8")).hexdigest()
