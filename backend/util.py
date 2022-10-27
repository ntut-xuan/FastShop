from enum import Enum

from flask import current_app


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


class Status(Enum):
    OK = {"status": "OK"}
    INVALID_DATA = {"status": "Failed", "code": 301}
    INVALID_EMAIL = {"status": "Failed", "code": 302}
    INVALID_PASSWORD = {"status": "Failed", "code": 303}
    INCORRECT_LOGIN = {"status": "Failed", "code": 401}
