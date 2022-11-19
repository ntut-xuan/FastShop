from dataclasses import dataclass
from http import HTTPStatus

from flask import current_app


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


def get_failed_message_by_HTTP_status(code) -> str:
    """This method can help you to get HTTP status message by HTTP status code.
    
    It can pass the failed message we wrote, otherwise, return the default description of HTTP status code.
    
    Attribute:
        code: HTTP status code.
    """
    
    failed_message_dict = {
        HTTPStatus.BAD_REQUEST.value: "The wrong format of data, the server can't understand the data.",
        HTTPStatus.UNPROCESSABLE_ENTITY.value: "The data format user post is correct, but the data is invalid.",
    }
    if code in failed_message_dict:
        return failed_message_dict[code]
    else:
        return HTTPStatus(code).description


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
            message = "OK" if code < 400 else get_failed_message_by_HTTP_status(code)
        self.message = {"message": message}

