from __future__ import annotations

from operator import attrgetter
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.sql.expression import Select

from database import db
from models import Item, Tag, TagOfItem

if TYPE_CHECKING:
    from flask import Flask


@pytest.fixture(autouse=True)
def insert_test_data(app: Flask) -> None:
    with app.app_context():
        db.session.execute(
            db.insert(Item),
            [
                {
                    "id": 1,
                    "name": "apple",
                    "count": 10,
                    "original": 30,
                    "discount": 25,
                    "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
                },
                {
                    "id": 2,
                    "name": "tilapia",
                    "count": 3,
                    "original": 50,
                    "discount": 45,
                    "avatar": "xx-S0m3-aVA7aR-0f-ti1a9iA-xx",
                },
            ],
        )
        db.session.execute(
            db.insert(Tag),
            [
                {"id": 1, "name": "fruit"},
                {"id": 2, "name": "fish"},
                {"id": 3, "name": "grocery"},
            ],
        )
        db.session.execute(
            db.insert(TagOfItem),
            [
                {"item_id": 1, "tag_id": 1},
                {"item_id": 2, "tag_id": 2},
                {"item_id": 1, "tag_id": 3},
                {"item_id": 2, "tag_id": 3},
            ],
        )
        db.session.commit()


def test_update_on_tag_should_be_cascaded_to_tag_of_item(app: Flask) -> None:
    # update the id of (2, "fish") to 5
    with app.app_context():
        id_of_fish_tag = 2
        db.session.execute(db.update(Tag).where(Tag.id == id_of_fish_tag).values(id=5))
        db.session.commit()

    # "tilapia" should now have a tag with id 5, which is "fish"
    with app.app_context():
        id_of_tilapia = 2
        stmt: Select = db.select(TagOfItem.tag_id).where(
            TagOfItem.item_id == id_of_tilapia
        )
        tag_ids_of_tilapia = list(
            map(attrgetter("tag_id"), db.session.execute(stmt).fetchall())
        )
        assert 5 in tag_ids_of_tilapia


def test_update_on_item_should_be_cascaded_to_tag_of_item(app: Flask) -> None:
    # update the id of item (1, "apple") to 3
    with app.app_context():
        id_of_apple_item = 1
        db.session.execute(
            db.update(Item).where(Item.id == id_of_apple_item).values(id=3)
        )
        db.session.commit()

    # "fruit" should now have a item with id 3, which is "apple"
    with app.app_context():
        id_of_fruit = 1
        stmt: Select = db.select(TagOfItem.item_id).where(
            TagOfItem.tag_id == id_of_fruit
        )
        item_ids_of_fruit = list(
            map(attrgetter("item_id"), db.session.execute(stmt).fetchall())
        )
        assert 3 in item_ids_of_fruit


def test_delete_on_tag_should_be_cascaded_to_tag_of_item(app: Flask) -> None:
    # delete the (2, "fish") tag
    with app.app_context():
        id_of_fish_tag = 2
        db.session.execute(db.delete(Tag).where(Tag.id == id_of_fish_tag))
        db.session.commit()

    # tilapia should no longer have a tag with id 2
    with app.app_context():
        id_of_tilapia = 2
        stmt: Select = db.select(TagOfItem.tag_id).where(
            TagOfItem.item_id == id_of_tilapia
        )
        tag_ids_of_tilapia = set(
            map(attrgetter("tag_id"), db.session.execute(stmt).fetchall())
        )
        assert tag_ids_of_tilapia == set([3])


def test_delete_on_item_should_be_cascaded_to_tag_of_item(app: Flask) -> None:
    # delete the item "apple", which has id 1
    with app.app_context():
        id_of_apple_tag = 1
        db.session.execute(db.delete(Item).where(Item.id == id_of_apple_tag))
        db.session.commit()

    # fruit should no longer have a item with id 1
    with app.app_context():
        id_of_fruit = 1
        stmt: Select = db.select(TagOfItem.item_id).where(
            TagOfItem.tag_id == id_of_fruit
        )
        item_ids_of_fruit = set(
            map(attrgetter("item_id"), db.session.execute(stmt).fetchall())
        )
        assert item_ids_of_fruit == set()
