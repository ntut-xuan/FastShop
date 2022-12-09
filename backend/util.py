import re
from dataclasses import dataclass

from flasgger import swag_from
from flask import Blueprint, current_app


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


def register_swagger_file(type: str, filename: str, methods: list[str] = None):
    """Formats the file path by type and filename to the URI format `../api/{type}/{filename}.yml`.

    The decorator to warp `swag_from` function from [flasgger](https://github.com/flasgger/flasgger).

    As long as the location and name of the files follow the convention,
    it can help you format the URI without passing it by yourself and causing redundancy.

    Arguments:
        type: The API type.
        filename: The filename of API documentation.
    """

    def wrapper(func):
        swag_from_function = swag_from(
            f"../api/{type}/{filename}.yml", methods=methods
        )(func)
        return swag_from_function

    return wrapper


def route_with_doc(bp: Blueprint, rule: str, methods: list[str]):
    def remove_angle_bracket_and_type(m: re.Match) -> str:
        # find typed params
        match: list[str] = re.findall(r"<[^<>]+:([^<>]+)>", m[0])
        if match:
            return match[0]
        # find untyped params
        match = re.findall(r"<([^<>]+)>", m[0])
        if match:
            return match[0]
        return ""

    rule = re.sub(r"<([^<>]+)>", remove_angle_bracket_and_type, rule)

    def wrapper(func):
        for method in methods:
            swag_from(f"../api/{bp.name}{rule}/{method.lower()}.yml", methods=[method])(
                func
            )
        return bp.route(rule, methods=methods)(func)

    return wrapper


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
