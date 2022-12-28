from typing import TYPE_CHECKING, Any

from pydantic import StrictInt, StrictStr, Field

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    # Fixes "Unexpected keyword argument" for custom dataclasses.
    # See https://github.com/python/mypy/issues/6239.
    from pydantic.dataclasses import dataclass


class PayloadTypeChecker:
    @dataclass
    class Item:
        avatar: StrictStr = Field(default="")
        count: StrictInt = Field(default=0)
        description: StrictStr = Field(default="")
        name: StrictStr = Field(default="")
        original: StrictInt = Field(default=0)
        discount: StrictInt = Field(default=0)
        id: StrictInt = Field(default=0)

    @dataclass
    class Tag:
        id: StrictInt = Field(default=0)
        name: StrictStr = Field(default="")


def flatten_item_payload(payload: dict[str, Any]) -> dict[str, Any]:
    flat_payload: dict[str, Any] = {
        "avatar": payload["avatar"],
        "count": payload["count"],
        "description": payload["description"],
        "name": payload["name"],
        "original": payload["price"]["original"],
        "discount": payload["price"]["discount"],
    }
    return flat_payload
