from flask import current_app
from enum import Enum


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


class Status(Enum):
    OK = {"status": "OK"}
    INVALID_DATA = {"status": "Failed", "message": "Invalid data.", "code": 301}
    INVALID_EMAIL = {"status": "Failed", "message": "Invalid e-mail.", "code": 302}
    INVALID_PASSWORD = {"status": "Failed", "message": "Invalid password.", "code": 303}
    INCORRECT_LOGIN = {"status": "Failed", "message": "Incorrect e-mail or password.", "code": 401}
