from __future__ import annotations

from typing import Final, TYPE_CHECKING

import pytest
from sqlalchemy.sql.expression import Select

from database import db
from models import Item, Tag, TagOfItem

if TYPE_CHECKING:
    from flask import Flask


class TestCascadeUpdateAndDeleteOnTagOfItem:
    @pytest.fixture(autouse=True)
    def insert_test_data(self, app: Flask) -> None:
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

    def test_update_on_tag_should_be_cascaded_to_tag_of_item(self, app: Flask) -> None:
        # update the id of (2, "fish") to 5
        original_id_of_fish_tag: Final = 2
        updated_id_of_fish_tag: Final = 5
        with app.app_context():
            db.session.execute(
                db.update(Tag)
                .where(Tag.id == original_id_of_fish_tag)
                .values(id=updated_id_of_fish_tag)
            )
            db.session.commit()

        # "tilapia" should now have a tag with id 5, which is "fish"
        with app.app_context():
            id_of_tilapia: Final = 2
            stmt: Select = db.select(TagOfItem.tag_id).where(
                TagOfItem.item_id == id_of_tilapia
            )
            tag_ids_of_tilapia: list[int] = db.session.execute(stmt).scalars().all()

            assert updated_id_of_fish_tag in tag_ids_of_tilapia

    def test_update_on_item_should_be_cascaded_to_tag_of_item(self, app: Flask) -> None:
        # update the id of item (1, "apple") to 3
        original_id_of_apple_item: Final = 1
        updated_id_of_apple_item: Final = 3
        with app.app_context():
            db.session.execute(
                db.update(Item)
                .where(Item.id == original_id_of_apple_item)
                .values(id=updated_id_of_apple_item)
            )
            db.session.commit()

        # "fruit" should now have a item with id 3, which is "apple"
        with app.app_context():
            id_of_fruit: Final = 1
            stmt: Select = db.select(TagOfItem.item_id).where(
                TagOfItem.tag_id == id_of_fruit
            )
            item_ids_of_fruit: list[int] = db.session.execute(stmt).scalars().all()

            assert updated_id_of_apple_item in item_ids_of_fruit

    def test_delete_on_tag_should_be_cascaded_to_tag_of_item(self, app: Flask) -> None:
        # delete the (2, "fish") tag
        id_of_fish_tag: Final = 2
        with app.app_context():
            db.session.execute(db.delete(Tag).where(Tag.id == id_of_fish_tag))
            db.session.commit()

        # tilapia should no longer have a tag with id 2
        with app.app_context():
            id_of_tilapia: Final = 2
            stmt: Select = db.select(TagOfItem.tag_id).where(
                TagOfItem.item_id == id_of_tilapia
            )
            tag_ids_of_tilapia: list[int] = db.session.execute(stmt).scalars().all()
            assert id_of_fish_tag not in tag_ids_of_tilapia

    def test_delete_on_item_should_be_cascaded_to_tag_of_item(self, app: Flask) -> None:
        # delete the item "apple", which has id 1
        id_of_apple_tag: Final = 1
        with app.app_context():
            db.session.execute(db.delete(Item).where(Item.id == id_of_apple_tag))
            db.session.commit()

        # fruit should no longer have a item with id 1
        with app.app_context():
            id_of_fruit: Final = 1
            stmt: Select = db.select(TagOfItem.item_id).where(
                TagOfItem.tag_id == id_of_fruit
            )
            item_ids_of_fruit: list[int] = db.session.execute(stmt).scalars().all()

            assert id_of_apple_tag not in item_ids_of_fruit


def test_item_discount_should_be_as_same_as_original_if_not_given(app: Flask) -> None:
    original: Final = 30
    with app.app_context():
        db.session.execute(
            db.insert(Item).values(
                id=1,
                name="apple",
                count=10,
                original=original,
                # no discount,
                avatar="xx-S0m3-aVA7aR-0f-a991e-xx",
            ),
        )
        db.session.commit()

    with app.app_context():
        select_discount_stmt: Select = db.select(Item.discount).where(Item.id == 1)
        discount: int = db.session.execute(select_discount_stmt).scalar_one()

        assert discount == original
