from dataclasses import dataclass
from http import HTTPStatus

from flask import current_app


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


@dataclass
class SingleMessageStatus:
    """A convenient response status dataclass.

    The message can be directly passed for responses with mimetype in json.

    Attributes:
        code: HTTP status code.
        message: A dict with a single key "message".
    """

    code: int
    message: dict[str, str]

    def __init__(self, code: int, message: str | None = None) -> None:
        """
        Args:
            code:
                HTTP status code.
            message:
                The response message to be wrapped into the message dict.
                Default to "OK" if code is lower than 400, otherwise, return the failed message.
        """
        self.code: int = code
        if message is None:
            message = "OK" if code < 400 else ""
        self.message = {"message": message}
