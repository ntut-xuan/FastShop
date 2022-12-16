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
        price=PriceData(
            original=item_data_dict["price"]["original"],
            discount=item_data_dict["price"]["discount"],
        ),
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
    new_item = Item(
        avatar=data.avatar,
        count=data.count,
        discount=data.price.discount,
        name=data.name,
        original=data.price.original,
    )

    db.session.add(new_item)
    db.session.flush()
    id: int = new_item.id

    db.session.commit()
    return id


def update_item_with_specific_id(
    id: int,
    avatar: str | None = None,
    count: int | None = None,
    discount: int | None = None,
    name: str | None = None,
    original: int | None = None,
) -> None:
    update_value = {
        "avatar": avatar,
        "count": count,
        "discount": discount,
        "name": name,
        "original": original,
    }

    # Delete all key with None value.
    for key, value in dict(update_value).items():
        if value is None:
            del update_value[key]

    update_data_stmts: Update = (
        db.update(Item).values(update_value).where(Item.id == id)
    )
    db.session.execute(update_data_stmts)
    db.session.commit()


def has_item_with_specific_id(id: int) -> bool:
    select_data_stmts: Select = (
        db.select([func.count(Item.id)]).select_from(Item).where(Item.id == id)
    )
    count: int = db.session.execute(select_data_stmts).scalar()
    return count > 0
