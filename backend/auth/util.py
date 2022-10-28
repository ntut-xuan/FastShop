import hashlib
import re
import jwt
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import IntEnum
from typing import Final

from auth.exception import EmailAlreadyRegisteredError, IncorrectEmailOrPasswordError
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


def register(email: str, password: str, profile: UserProfile) -> None:
    """
    Raises:
        EmailAlreadyRegisteredError: `email` should not be already registered.
    """

    if is_registered(email):
        raise EmailAlreadyRegisteredError

    stmt_to_insert_new_user: str = """
        INSERT INTO `user`(`email`, `password`, `firstname`, `lastname`, `gender`, `birthday`)
            VALUES(?, ?, ?, ?, ?, ?)
    """
    execute_command(
        stmt_to_insert_new_user,
        (
            email,
            hash_with_sha512(password),
            profile.firstname,
            profile.lastname,
            profile.gender,
            profile.birthday,
        ),
    )


def is_correct_password(registered_email: str, password_to_check: str) -> bool:
    """The `registered_email` should be already registered, otherwise Exception raised by the database."""
    hashed_password_to_check = hash_with_sha512(password_to_check)
    hashed_user_password: int = execute_command(
        "SELECT `password` FROM `user` WHERE `email` = ?",
        (registered_email,),
    )[0]["password"]

    return hashed_password_to_check == hashed_user_password


def is_registered(email: str) -> bool:
    """Returns whether the email is aldready used."""
    user_count: int = execute_command(
        "SELECT COUNT(*) as `user_count` FROM `user` WHERE `email` = ?",
        (email,),
    )[0]["user_count"]

    return user_count != 0


def hash_with_sha512(string: str) -> str:
    return hashlib.sha512(string.encode("utf-8")).hexdigest()


def is_valid_jwt_data(data: str) -> bool:
    """Return the jwt data is valid or not."""
    if data is None:
        return False

    decode_data = jwt.decode(data, "secret", algorithms=["HS256"])
    expire_time = decode_data["exp"]
    current_time = datetime.now(tz=timezone.utc).timestamp()

    if current_time > expire_time:
        return False

    return True


def generate_payload(
    data: dict, expire_time_delta: timedelta = timedelta(days=1)
) -> str:
    """Return the payload with generate time attribute (iat) and 1 day expired strict attribute (exp)."""
    current_time: datetime = datetime.now(tz=timezone.utc)
    expire_time = current_time + expire_time_delta
    payload = {
        "data": data,
        "iat": current_time,
        "exp": expire_time,
    }
    jwt_data = jwt.encode(payload, "secret", algorithm="HS256")
    return jwt_data


def decode_jwt(data: str) -> dict:
    """Return the decoded jwt data, the jwt data should be exist."""
    return jwt.decode(data, "secret", algorithms=["HS256"])
