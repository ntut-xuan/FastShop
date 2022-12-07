from dataclasses import dataclass
from http import HTTPStatus

from flask import current_app
from flasgger import swag_from


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


def register_swagger_file(type: str, filename: str, methods: list[str] = None):
    """The decorator to warp `swag_from` function from flasgger.

    It can format the file path by type and filename to the URI format below:

    `../api/{type}/{filename}.yml`

    So as long as the location and name of the files follow the convention,
    it can help you format the URI without passing it by yourself and causing redundancy.

    Arguments:
        type: The API type.
        filename: The filename of API documentation.
    """

    def warpper(func):
        swag_from_function = swag_from(
            f"../api/{type}/{filename}.yml", methods=methods
        )(func)
        return swag_from_function

    return warpper


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
                Default to "OK" if code is lower than 400, otherwise, an empty message.
        """
        self.code: int = code
        if message is None:
            message = "OK" if code < 400 else ""
        self.message = {"message": message}
