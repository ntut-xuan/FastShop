from functools import wraps
from http import HTTPStatus
from typing import Any, Callable, TypeVar, cast

from flask import Response, request
from pydantic import StrictInt
from pydantic.dataclasses import dataclass

from response_message import INVALID_DATA, WRONG_DATA_FORMAT
from src.models import Item, ShoppingCart
from src.shopping_cart.util import fetch_user_id_from_jwt_token
from util import make_single_message_response

T = TypeVar("T")


def validate_count_should_positive_or_return_unprocessable_entity(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)

        assert payload is not None

        if payload["count"] < 0:
            return make_single_message_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, str("Count should be positive.")
            )

        return func(*args, **kwargs)

    return wrapper


def validate_format_or_return_bad_request(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)

        assert payload is not None

        @dataclass
        class Validator:
            count: Any
            id: Any

        try:
            Validator(**payload)
        except TypeError:
            return make_single_message_response(
                HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT
            )

        return func(*args, **kwargs)

    return wrapper


def validate_data_type_or_return_unprocessable_entity(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)

        assert payload is not None

        @dataclass
        class Validator:
            count: StrictInt
            id: StrictInt

        try:
            Validator(**payload)
        except ValueError:
            return make_single_message_response(
                HTTPStatus.UNPROCESSABLE_ENTITY, INVALID_DATA
            )

        return func(*args, **kwargs)

    return wrapper


def validate_item_exists_or_return_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)

        assert payload is not None

        item: Item | None = Item.query.filter_by(id=payload["id"]).first()

        if item is None:
            return make_single_message_response(
                HTTPStatus.FORBIDDEN, "Item with specific ID does not exists."
            )

        return func(*args, **kwargs)

    return wrapper


def validate_item_exists_in_user_cart_or_return_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        jwt_token: str | None = request.cookies.get("jwt")

        assert payload is not None
        assert jwt_token is not None

        user_id = fetch_user_id_from_jwt_token(jwt_token)
        item: Item = ShoppingCart.query.filter_by(
            item_id=payload["id"], user_id=user_id
        ).first()
        if item is None:
            return make_single_message_response(
                HTTPStatus.FORBIDDEN,
                "Item with specific ID is not exist in shopping cart.",
            )

        return func(*args, **kwargs)

    return wrapper


def validate_item_not_exists_in_user_cart_or_return_forbidden(
    func: Callable[..., Response | T]
) -> Callable[..., Response | T]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response | T:
        payload: dict[str, Any] | None = request.get_json(silent=True)
        jwt_token: str | None = request.cookies.get("jwt")

        assert payload is not None
        assert jwt_token is not None

        user_id = fetch_user_id_from_jwt_token(jwt_token)
        item: Item = ShoppingCart.query.filter_by(
            item_id=payload["id"], user_id=user_id
        ).first()
        if item is not None:
            return make_single_message_response(
                HTTPStatus.FORBIDDEN,
                "Item with specific ID is not exist in shopping cart.",
            )

        return func(*args, **kwargs)

    return wrapper
