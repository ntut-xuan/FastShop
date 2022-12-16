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


def covert_item_object(item_data_dict: dict[str, Any]):
    item = ItemData(
        avatar=item_data_dict["avatar"],
        count=item_data_dict["count"],
        name=item_data_dict["name"],
        price=PriceData(original=item_data_dict["price"]["original"]),
    )
    if "discount" in item_data_dict["price"]:
        item.price.discount = item_data_dict["price"]["discount"]
    if "tags" in item_data_dict:
        item.tags = convert_tags_object_list(item_data_dict["tags"])
    return item


def convert_tags_object_list(tags_dict_list: list[dict[str, Any]]):
    tags_object_list = []

    for tags_data in tags_dict_list:
        tags_object_list.append(TagData(id=tags_data["id"], name=tags_data["name"]))

    return tags_object_list
