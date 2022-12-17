from typing import TYPE_CHECKING, Any

from pydantic import Field, StrictInt, StrictStr
from sqlalchemy import func

from database import db
from item.exception import ItemNotExistError
from models import Item, Tag, TagOfItem

if TYPE_CHECKING:
    from dataclasses import dataclass

    from sqlalchemy.sql.dml import Delete, Insert, Update
    from sqlalchemy.sql.selectable import Select
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


def convert_item_object(item_data_dict: dict[str, Any]) -> ItemData:
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
    if not has_item_with_specific_id(id):
        raise ItemNotExistError

    update_value: dict[str, Any] = {
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


def get_item_with_specific_id(id: int) -> ItemData:
    if not has_item_with_specific_id(id):
        raise ItemNotExistError

    select_item_data_stmts: Select = (
        db.select(["*"]).select_from(Item).where(Item.id == id)
    )
    select_tag_of_item_data_stmts: Select = (
        db.select([Tag.id, Tag.name])
        .select_from(Tag)
        .join(TagOfItem)
        .where(TagOfItem.item_id == id)
    )

    query_item: tuple = db.session.execute(select_item_data_stmts).one()
    query_tag_of_item: list[tuple] = db.session.execute(
        select_tag_of_item_data_stmts
    ).fetchall()

    query_item_data: ItemData = convert_database_tuple_to_item_data(query_item)
    query_tag_object_list: list[TagData] = convert_tuple_list_to_tag_object_list(
        query_tag_of_item
    )

    query_item_data.tags = query_tag_object_list
    return query_item_data


def get_all_items() -> list[ItemData]:
    select_data_stmts: Select = db.select(["*"]).select_from(Item)
    query_item_list: list[tuple] = db.session.execute(select_data_stmts).fetchall()
    query_item_data_list: list[ItemData] = [
        convert_database_tuple_to_item_data(query_item_tuple)
        for query_item_tuple in query_item_list
    ]
    return query_item_data_list


def delete_item_with_specific_id(id: int) -> None:
    if not has_item_with_specific_id(id):
        raise ItemNotExistError

    delete_data_stmts: Delete = db.delete(Item).where(Item.id == id)
    db.session.execute(delete_data_stmts)
    db.session.commit()


def has_item_with_specific_id(id: int) -> bool:
    select_data_stmts: Select = (
        db.select([func.count(Item.id)]).select_from(Item).where(Item.id == id)
    )
    count: int = db.session.execute(select_data_stmts).scalar()
    return count > 0


def convert_database_tuple_to_item_data(item: tuple) -> ItemData:
    return ItemData(
        item[5],  # Column 6 is avatar
        item[2],  # Column 3 is count
        item[1],  # Column 2 is name
        PriceData(item[3], item[4]),  # Column 4, 5 is discount, original price
    )


def convert_tuple_list_to_tag_object_list(tag_tuple_list: list[tuple]) -> list[Tag]:
    tag_object_list: list[TagData] = [
        TagData(id=tag_tuple[0], name=tag_tuple[1]) for tag_tuple in tag_tuple_list
    ]
    return tag_object_list
