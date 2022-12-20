from typing import Any

from pydantic import StrictInt, StrictStr, Field
from pydantic.dataclasses import dataclass


class PayloadTypeChecker:
    @dataclass
    class Item:
        avatar: StrictStr
        count: StrictInt
        name: StrictStr
        original: StrictInt
        discount: StrictInt
        id: StrictInt = Field(default=0)

    @dataclass
    class Tag:
        id: StrictInt
        name: StrictStr = Field(default="")


def flatten_item_payload(payload: dict[str, Any]) -> dict[str, Any]:
    flat_payload: dict[str, Any] = {
        "avatar": payload["avatar"],
        "count": payload["count"],
        "name": payload["name"],
        "original": payload["price"]["original"],
        "discount": payload["price"]["discount"],
    }
    return flat_payload
