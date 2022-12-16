from typing import TYPE_CHECKING, Any

from pydantic import Field, StrictInt, StrictStr

if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass


@dataclass
class PriceData:
    original: StrictInt
    discount: StrictInt | None = Field(None)


@dataclass
class TagData:
    id: StrictInt
    name: StrictStr


@dataclass
class ItemData:
    avatar: StrictStr
    count: StrictInt
    name: StrictStr
    price: PriceData
    tags: list[TagData] = Field([])


def get_item_object_from_item_data_dict(dict: dict[str, Any]):
    item = ItemData(
        avatar=dict["avatar"],
        count=dict["count"],
        name=dict["name"],
        price=PriceData(original=dict["price"]["original"]),
    )
    if "discount" in dict["price"]:
        item.price.discount = dict["price"]["discount"]
    if "tags" in dict:
        item.tags = [
            TagData(id=tags_data["id"], name=tags_data["name"])
            for tags_data in dict["tags"]
        ]
    return item
