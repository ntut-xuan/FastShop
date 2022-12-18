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


@dataclass
class ItemDataWithTags(ItemData):
    tags: list[TagData]


def convert_item_data_dict_to_item_data(item_data_dict: dict[str, Any]) -> ItemData:
    item = ItemData(
        avatar=item_data_dict["avatar"],
        count=item_data_dict["count"],
        name=item_data_dict["name"],
        price=PriceData(
            original=item_data_dict["price"]["original"],
            discount=item_data_dict["price"]["discount"],
        ),
    )
    return item


def convert_tags_object_list(tags_dict_list: list[dict[str, Any]]) -> list[TagData]:
    tags_object_list = []

    for tags_data in tags_dict_list:
        tags_object_list.append(TagData(id=tags_data["id"], name=tags_data["name"]))

    return tags_object_list


def add_tags_to_item_data(
    item_data: ItemData, tags_list: list[TagData]
) -> ItemDataWithTags:
    item_data_with_tags = ItemDataWithTags(
        avatar=item_data.avatar,
        count=item_data.count,
        name=item_data.name,
        price=PriceData(
            original=item_data.price.original,
            discount=item_data.price.discount,
        ),
        tags=tags_list,
    )
    return item_data_with_tags


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


def get_item_with_specific_id(id: int) -> ItemDataWithTags:
    if not has_item_with_specific_id(id):
        raise ItemNotExistError

    select_item_data_stmts: Select = (
        db.select(["*"]).select_from(Item).where(Item.id == id)
    )

    query_item: tuple = db.session.execute(select_item_data_stmts).one()

    query_item_data: ItemData = convert_database_tuple_to_item_data(query_item)
    query_tag_object_list: list[TagData] = get_all_tags_with_specific_item_id(id)

    query_item_data_with_tags: ItemDataWithTags = add_tags_to_item_data(
        query_item_data, query_tag_object_list
    )
    return query_item_data_with_tags


def get_all_items() -> list[ItemDataWithTags]:
    select_data_stmts: Select = db.select(["*"]).select_from(Item)
    query_item_list: list[tuple] = db.session.execute(select_data_stmts).fetchall()
    query_item_data_with_tags_list: list[ItemDataWithTags] = []

    for item_data_tuple in query_item_list:
        item_data = convert_database_tuple_to_item_data(item_data_tuple)
        tag_object_list = get_all_tags_with_specific_item_id(
            item_data_tuple[0]
        )  # 0 for id.
        item_data_with_tags = add_tags_to_item_data(item_data, tag_object_list)
        query_item_data_with_tags_list.append(item_data_with_tags)

    return query_item_data_with_tags_list


def get_all_tags_with_specific_item_id(id: int) -> list[TagData]:
    select_tag_of_item_data_stmts: Select = (
        db.select([Tag.id, Tag.name])
        .select_from(Tag)
        .join(TagOfItem)
        .where(TagOfItem.item_id == id)
    )
    query_tag_of_item: list[tuple] = db.session.execute(
        select_tag_of_item_data_stmts
    ).fetchall()
    query_tag_object_list: list[TagData] = convert_tuple_list_to_tag_object_list(
        query_tag_of_item
    )
    return query_tag_object_list


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


def setup_tags_relationship_of_item(item_id: int, tags_id_list: list[int]):
    # Step 1. Drop all tags of item if exists.
    delete_tags_stmts: Delete = db.delete(TagOfItem).where(TagOfItem.item_id == item_id)
    db.session.execute(delete_tags_stmts)
    db.session.commit()

    # Step 2. Insert all tags relationship
    for tag_id in tags_id_list:
        db.session.add(TagOfItem(item_id=item_id, tag_id=tag_id))
    db.session.commit()


def convert_database_tuple_to_item_data(item: tuple) -> ItemData:
    return ItemData(
        item[5],  # Column 6 is avatar
        item[2],  # Column 3 is count
        item[1],  # Column 2 is name
        PriceData(item[3], item[4]),  # Column 4, 5 is discount, original price
    )


def convert_tuple_list_to_tag_object_list(tag_tuple_list: list[tuple]) -> list[TagData]:
    tag_object_list: list[TagData] = [
        TagData(id=tag_tuple[0], name=tag_tuple[1]) for tag_tuple in tag_tuple_list
    ]
    return tag_object_list
