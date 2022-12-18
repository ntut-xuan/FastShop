from __future__ import annotations

from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

import pytest
from pydantic.error_wrappers import ValidationError
from sqlalchemy import func

from database import db
from item.exception import ItemNotExistError
from item.util import (
    ItemData,
    ItemDataWithTags,
    PriceData,
    TagData,
    add_item_data,
    add_tags_to_item_data,
    convert_database_tuple_to_item_data,
    convert_item_data_dict_to_item_data,
    convert_tags_object_list,
    delete_item_with_specific_id,
    get_all_items,
    get_item_with_specific_id,
    has_item_with_specific_id,
    update_item_with_specific_id,
)
from models import Item, Tag, TagOfItem

if TYPE_CHECKING:
    from flask import Flask
    from sqlalchemy.sql.selectable import Select


@dataclass
class ItemIdPackage:
    item_id: int
    another_item_id: int


@pytest.fixture
def item_data_dict() -> dict:
    return {
        "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
        "count": 44,
        "name": "Entropy",
        "price": {"discount": 43210, "original": 48763},
        "tags": [{"id": 33, "name": "dian"}],
    }


def is_item_tuple_and_item_data_object_equals(item: tuple, item_data: ItemData) -> bool:
    compare_result: bool = convert_database_tuple_to_item_data(item) == item_data
    return compare_result


@pytest.fixture
def item_data(item_data_dict: dict[str, Any]) -> ItemDataWithTags:
    converted_item: ItemData = convert_item_data_dict_to_item_data(item_data_dict)
    converted_tags_list: list[TagData] = convert_tags_object_list(
        item_data_dict["tags"]
    )
    item_data_with_tags: ItemDataWithTags = add_tags_to_item_data(
        converted_item, converted_tags_list
    )
    return item_data_with_tags


@pytest.fixture
def another_item_data() -> ItemDataWithTags:
    another_item_data: dict = {
        "avatar": "f32aa7ea-c092-4e92-b4c9-d4b41141fd7d",
        "count": 66,
        "name": "Entropy-2",
        "price": {"discount": 98765, "original": 90000},
        "tags": [{"id": 44, "name": "more-dian"}],
    }
    converted_item: ItemData = convert_item_data_dict_to_item_data(another_item_data)
    converted_tags_list: list[TagData] = convert_tags_object_list(
        another_item_data["tags"]
    )
    item_data_with_tags: ItemDataWithTags = add_tags_to_item_data(
        converted_item, converted_tags_list
    )
    return item_data_with_tags


@pytest.fixture
def place_item(
    app: Flask, item_data_dict: dict[str, Any], another_item_data: ItemDataWithTags
) -> ItemIdPackage:
    with app.app_context():
        # Two different item will be place, item_data and another_item_data.
        item_data_object: ItemData = convert_item_data_dict_to_item_data(item_data_dict)
        another_item_data_object: ItemData = another_item_data

        # Add item to database
        item_data_id: int = add_item_data(item_data_object)
        another_item_data_id: int = add_item_data(another_item_data_object)

        # Add their tag to database
        item_data_tag = Tag(id=33, name="dian")
        another_item_data_tag = Tag(id=44, name="more-dian")
        db.session.add(item_data_tag)
        db.session.add(another_item_data_tag)

        # Add their relationship
        item_object_tag_of_item = TagOfItem(item_id=item_data_id, tag_id=33)
        another_item_object_tag_of_item = TagOfItem(
            item_id=another_item_data_id, tag_id=44
        )
        db.session.add(item_object_tag_of_item)
        db.session.add(another_item_object_tag_of_item)
        db.session.commit()

        return ItemIdPackage(item_data_id, another_item_data_id)


class TestCovertItemDataObjectFromItemDataDict:
    def test_valid_dict_should_return_correct_item_object(
        self, item_data_dict: dict[str, Any]
    ):
        item_data: ItemData = convert_item_data_dict_to_item_data(item_data_dict)

        assert item_data.avatar == "f692073a-7ac1-11ed-a1eb-0242ac120002"
        assert item_data.count == 44
        assert item_data.name == "Entropy"
        assert item_data.price.discount == 43210
        assert item_data.price.original == 48763

    def test_incorrect_format_dict_should_raise_missing_fields_error(self):
        with pytest.raises(KeyError):
            convert_item_data_dict_to_item_data({"wrong_column": "wrong_value"})

    def test_invalid_data_dict_should_raise_error(self, item_data_dict: dict[str, Any]):
        item_data_dict[
            "count"
        ] = "5"  # Since count require integer-type data, it should cause error.

        with pytest.raises(ValidationError):
            convert_item_data_dict_to_item_data(item_data_dict)

    def test_no_tags_dict_should_ok(self, item_data_dict: dict[str, Any]):
        del item_data_dict["tags"]

        convert_item_data_dict_to_item_data(item_data_dict)


class TestItemManipulation:
    def test_add_item_should_ok(self, app: Flask, item_data: ItemDataWithTags):
        with app.app_context():

            id = add_item_data(item_data)

            query_item_data: ItemDataWithTags = get_item_with_specific_id(id)
            query_item_data_with_tags: ItemDataWithTags = add_tags_to_item_data(
                query_item_data, item_data.tags
            )
            assert query_item_data_with_tags == item_data

    def test_check_count_of_non_exist_id_should_return_false(self, app: Flask):
        with app.app_context():

            assert has_item_with_specific_id(111111) == False

    def test_check_count_of_exist_id_should_return_true(
        self, app: Flask, place_item: ItemIdPackage
    ):
        place_item_id = place_item.item_id
        with app.app_context():

            assert has_item_with_specific_id(place_item_id)

    def test_update_item_with_absent_id_should_raise_error(self, app: Flask):
        with app.app_context():

            with pytest.raises(ItemNotExistError):
                update_item_with_specific_id(65536)

    def test_update_all_item_column_value_should_ok(
        self, app: Flask, place_item: ItemIdPackage, another_item_data: ItemData
    ):
        place_item_id = place_item.item_id
        with app.app_context():

            update_item_with_specific_id(
                place_item_id,
                avatar=another_item_data.avatar,
                count=another_item_data.count,
                discount=another_item_data.price.discount,
                name=another_item_data.name,
                original=another_item_data.price.original,
            )
            query_item_data: ItemDataWithTags = get_item_with_specific_id(place_item_id)

            assert query_item_data == another_item_data

    def test_update_part_of_item_column_value_should_ok(
        self,
        app: Flask,
        place_item: ItemIdPackage,
        item_data: ItemData,
        another_item_data: ItemData,
    ):
        place_item_id = place_item.item_id
        with app.app_context():

            update_item_with_specific_id(
                place_item_id,
                avatar=another_item_data.avatar,
                count=another_item_data.count,
            )
            query_item_data: ItemData = get_item_with_specific_id(place_item_id)

            prepare_compare_item_data = item_data
            prepare_compare_item_data.avatar = another_item_data.avatar
            prepare_compare_item_data.count = another_item_data.count

            assert query_item_data == prepare_compare_item_data

    def test_get_item_by_absent_id_should_raise_error(self, app: Flask):
        with app.app_context():

            with pytest.raises(ItemNotExistError):
                get_item_with_specific_id(65536)

    def test_get_item_by_exist_id_should_return_item_data_object(
        self, app: Flask, item_data: ItemData, place_item: ItemIdPackage
    ):
        place_item_id = place_item.item_id
        with app.app_context():

            query_item_data: ItemData = get_item_with_specific_id(place_item_id)

            assert query_item_data == item_data

    def test_get_all_item_should_return_item_data_object_list(
        self, app: Flask, item_data: ItemDataWithTags, place_item: ItemIdPackage
    ):
        with app.app_context():

            query_item_data_list: list[ItemDataWithTags] = get_all_items()
            assert query_item_data_list[0] == item_data

    def test_delete_item_by_absent_id_should_raise_error(self, app: Flask):
        with app.app_context():

            with pytest.raises(ItemNotExistError):
                delete_item_with_specific_id(65536)

    def test_delete_item_by_exist_id_should_ok(
        self, app: Flask, place_item: ItemIdPackage
    ):
        place_item_id = place_item.item_id
        with app.app_context():

            delete_item_with_specific_id(place_item_id)

            assert not has_item_with_specific_id(place_item_id)
