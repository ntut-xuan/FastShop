from typing import TYPE_CHECKING, Any

from pydantic import Field, StrictInt, StrictStr
from sqlalchemy import func

from database import db
from models import Item


if TYPE_CHECKING:
    from dataclasses import dataclass
    from sqlalchemy.sql.selectable import Select
    from sqlalchemy.sql.dml import Insert, Update
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
    if "tags" in item_data_dict:
        item.tags = convert_tags_object_list(item_data_dict["tags"])
    return item


def convert_tags_object_list(tags_dict_list: list[dict[str, Any]]):
    tags_object_list = []

    for tags_data in tags_dict_list:
        tags_object_list.append(TagData(id=tags_data["id"], name=tags_data["name"]))

    return tags_object_list


def add_item_data(data: ItemData) -> int:
    insert_data_stmts: Insert = db.insert(Item).values(
        avatar=data.avatar,
        count=data.count,
        discount=data.price.discount,
        name=data.name,
        original=data.price.original,
    )
    db.session.execute(insert_data_stmts)
    db.session.commit()
    
    select_data_count_stmts: Select = db.select([func.count(Item.id)]).select_from(Item)
    id = db.session.execute(select_data_count_stmts).scalar_one()
    return id