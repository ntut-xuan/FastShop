import re


def validate_by_regex(data: str, regex: str) -> bool:
    return bool(re.match(regex, data))


def validate_email(email: str) -> bool:
    return validate_by_regex(email, "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")


def login(email: str, password: str) -> bool:
    if not validate_email(email):
        return False
    else:
        return True
