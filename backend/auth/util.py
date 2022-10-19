from database.util import execute_command
from hashlib import sha512

import re


def validate_by_regex(data: str, regex: str) -> bool:
    return bool(re.match(regex, data))


def validate_email(email: str) -> bool:
    return validate_by_regex(email, "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")


def login(email: str, password: str) -> bool:

    if not validate_email(email):
        return False

    m = sha512()
    m.update(password.encode("utf-8"))
    hash = m.hexdigest()
    user_count = execute_command(
        "SELECT COUNT(*) FROM `User` WHERE email=%s and password=%s", (email, hash)
    )[0]["COUNT(*)"]

    return user_count > 0
