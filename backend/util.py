import re
from dataclasses import dataclass

from flasgger import swag_from
from flask import Blueprint, current_app


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


def route_with_doc(bp: Blueprint, rule: str, methods: list[str]):
    """Decorates a view function to register it with the given URL rule and methods,
    and loads the swagger specs mapped by the URL rule.

    The swagger yml file of specs should be placed in `../api/` and have the same folder
    structure as the rule.
    """

    def remove_angle_bracket_and_param_type(m: re.Match) -> str:
        # one may use findall with patterns concatenated with '|',
        # but the return type will be complex as list[tuple[str, ...]]
        typed_params = r"<[^<>]+:([^<>]+)>"
        untyped_params = r"<([^<>]+)>"
        for pattern in (typed_params, untyped_params):
            match: list[str] = re.findall(pattern, m[0])
            if match:
                return match[0]
        raise RuntimeError("the pattern used with re.sub might be ill-formed")

    doc_path: str = re.sub(r"<([^<>]+)>", remove_angle_bracket_and_param_type, rule)

    def wrapper(func):
        for method in methods:
            swag_from(
                f"../api/{bp.name}{doc_path}/{method.lower()}.yml",
                methods=[method],
            )(func)
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
