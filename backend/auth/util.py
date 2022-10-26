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


def login(email: str, password: str) -> bool:
    hashed_password: str = hash_with_sha512(password)
    return is_registered(email, hashed_password)


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


def register(email: str, password: str, profile: UserProfile) -> bool:
    hashed_password: str = hash_with_sha512(password)

    if is_registered(email, hashed_password):
        return False

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
    return True


def hash_with_sha512(string: str) -> str:
    return hashlib.sha512(string.encode("utf-8")).hexdigest()


def is_registered(email: str, hashed_password: str) -> bool:
    user_count: int = execute_command(
        "SELECT COUNT(*) as `user_count` FROM `user` WHERE `email` = ? and `password` = ?",
        (email, hashed_password),
    )[0]["user_count"]

    return user_count != 0
