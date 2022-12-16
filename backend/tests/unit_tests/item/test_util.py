from __future__ import annotations

from typing import Any, TYPE_CHECKING

import pytest
from pydantic.error_wrappers import ValidationError
from sqlalchemy import func

from database import db
from item.exception import ItemNotExistError
from item.util import (
    ItemData,
    PriceData,
    TagData,
    add_item_data,
    covert_item_object,
    convert_tags_object_list,
    convert_database_tuple_to_item_data,
    delete_item_with_specific_id,
    get_item_with_specific_id,
    has_item_with_specific_id,
    update_item_with_specific_id,
)
from models import Item

if TYPE_CHECKING:
    from flask import Flask
    from sqlalchemy.sql.selectable import Select


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
    item_data.tags = (
        []
    )  # Query data doesn't have tags field, set compared item_data tags attribute to default.
    compare_result: bool = convert_database_tuple_to_item_data(item) == item_data
    return compare_result


def is_item_data_equals_another_item_data_without_tag_attribute(
    item_data: ItemData, another_item_data: ItemData
):
    item_data.tags = []
    another_item_data.tags = []
    return item_data == another_item_data


@pytest.fixture
def item_data(item_data_dict: dict[str, Any]) -> ItemData:
    converted_item: ItemData = covert_item_object(item_data_dict)
    return converted_item


@pytest.fixture
def another_item_data() -> ItemData:
    another_item_data: dict = {
        "avatar": "f32aa7ea-c092-4e92-b4c9-d4b41141fd7d",
        "count": 66,
        "name": "Entropy-2",
        "price": {"discount": 98765, "original": 90000},
        "tags": [{"id": 44, "name": "more-dian"}],
    }
    converted_item: ItemData = covert_item_object(another_item_data)
    return converted_item


@pytest.fixture
def place_item(app: Flask, item_data_dict: dict[str, Any]) -> int:
    with app.app_context():
        item_data_object: ItemData = covert_item_object(item_data_dict)
        return add_item_data(item_data_object)


class TestCovertItemDataObjectFromItemDataDict:
    def test_valid_dict_should_return_correct_item_object(
        self, item_data_dict: dict[str, Any]
    ):
        item: ItemData = covert_item_object(item_data_dict)

        assert item.avatar == "f692073a-7ac1-11ed-a1eb-0242ac120002"
        assert item.count == 44
        assert item.name == "Entropy"
        assert item.price.discount == 43210
        assert item.price.original == 48763
        assert item.tags[0].id == 33
        assert item.tags[0].name == "dian"

    def test_incorrect_format_dict_should_raise_missing_fields_error(self):
        with pytest.raises(KeyError):
            covert_item_object({"wrong_column": "wrong_value"})

    def test_invalid_data_dict_should_raise_error(self, item_data_dict: dict[str, Any]):
        item_data_dict[
            "count"
        ] = "5"  # Since count require integer-type data, it should cause error.

        with pytest.raises(ValidationError):
            covert_item_object(item_data_dict)

    def test_no_tags_dict_should_ok(self, item_data_dict: dict[str, Any]):
        del item_data_dict["tags"]

        covert_item_object(item_data_dict)


class TestItemManipulation:
    def test_tags_dict_list_convert_to_tags_object_list_should_ok(
        self, item_data_dict: dict[str, Any]
    ):
        tags_object_list = convert_tags_object_list(item_data_dict["tags"])

        assert isinstance(tags_object_list, list)
        for object in tags_object_list:
            assert isinstance(object, TagData)

    def test_add_item_should_ok(self, app: Flask, item_data: ItemData):
        with app.app_context():

            id = add_item_data(item_data)
            item_data_select_stmt: Select = (
                db.select(["*"]).select_from(Item).where(Item.id == id)
            )
            item: tuple = db.session.execute(item_data_select_stmt).one()

            assert is_item_tuple_and_item_data_object_equals(item, item_data)

    def test_check_count_of_non_exist_id_should_return_false(self, app: Flask):
        with app.app_context():

            assert has_item_with_specific_id(111111) == False

    def test_check_count_of_exist_id_should_return_true(
        self, app: Flask, place_item: int
    ):
        place_item_id = place_item
        with app.app_context():

            assert has_item_with_specific_id(place_item_id)

    def test_update_all_item_column_value_should_ok(
        self, app: Flask, place_item: int, another_item_data: ItemData
    ):
        place_item_id = place_item
        with app.app_context():

            update_item_with_specific_id(
                place_item_id,
                avatar=another_item_data.avatar,
                count=another_item_data.count,
                discount=another_item_data.price.discount,
                name=another_item_data.name,
                original=another_item_data.price.original,
            )
            item_data_select_stmt: Select = (
                db.select(["*"]).select_from(Item).where(Item.id == place_item_id)
            )
            query_item_data: tuple = db.session.execute(item_data_select_stmt).one()

            assert is_item_tuple_and_item_data_object_equals(
                query_item_data, another_item_data
            )

    def test_update_part_of_item_column_value_should_ok(
        self,
        app: Flask,
        place_item: int,
        item_data: ItemData,
        another_item_data: ItemData,
    ):
        place_item_id = place_item
        with app.app_context():

            update_item_with_specific_id(
                place_item_id,
                avatar=another_item_data.avatar,
                count=another_item_data.count,
            )
            item_data_select_stmt: Select = (
                db.select(["*"]).select_from(Item).where(Item.id == place_item_id)
            )
            query_item: tuple = db.session.execute(item_data_select_stmt).one()

            prepare_compare_item_data = item_data
            prepare_compare_item_data.avatar = another_item_data.avatar
            prepare_compare_item_data.count = another_item_data.count
            assert is_item_tuple_and_item_data_object_equals(
                query_item, prepare_compare_item_data
            )

    def test_get_item_by_absent_id_should_raise_error(self, app: Flask):
        with app.app_context():

            with pytest.raises(ItemNotExistError):
                get_item_with_specific_id(65536)

    def test_get_item_by_exist_id_should_return_item_data_object(
        self, app: Flask, item_data: ItemData, place_item: int
    ):
        place_item_id = place_item
        with app.app_context():

            query_item_data: ItemData = get_item_with_specific_id(place_item_id)

            assert is_item_data_equals_another_item_data_without_tag_attribute(
                query_item_data, item_data
            )

    def test_delete_item_by_absent_id_should_raise_error(self, app: Flask):
        with app.app_context():

            with pytest.raises(ItemNotExistError):
                delete_item_with_specific_id(65536)

    def test_delete_item_by_exist_id_should_ok(self, app: Flask, place_item: int):
        place_item_id = place_item
        with app.app_context():

            delete_item_with_specific_id(place_item_id)

            assert not has_item_with_specific_id(place_item_id)

    def test_update_all_item_column_value_should_ok(
        self, app: Flask, place_item: int, another_item_data: ItemData
    ):
        place_item_id = place_item
        with app.app_context():

            update_item_with_specific_id(
                place_item_id,
                avatar=another_item_data.avatar,
                count=another_item_data.count,
                discount=another_item_data.price.discount,
                name=another_item_data.name,
                original=another_item_data.price.original,
            )
            item_data_select_stmt: Select = (
                db.select(["*"]).select_from(Item).where(Item.id == place_item_id)
            )
            query_item_data: tuple = db.session.execute(item_data_select_stmt).one()

            assert is_item_tuple_and_item_data_object_equals(
                query_item_data, another_item_data
            )

    def test_update_part_of_item_column_value_should_ok(
        self,
        app: Flask,
        place_item: int,
        item_data: ItemData,
        another_item_data: ItemData,
    ):
        place_item_id = place_item
        with app.app_context():

            update_item_with_specific_id(
                place_item_id,
                avatar=another_item_data.avatar,
                count=another_item_data.count,
            )
            item_data_select_stmt: Select = (
                db.select(["*"]).select_from(Item).where(Item.id == place_item_id)
            )
            query_item: tuple = db.session.execute(item_data_select_stmt).one()

            prepare_compare_item_data = item_data
            prepare_compare_item_data.avatar = another_item_data.avatar
            prepare_compare_item_data.count = another_item_data.count
            assert is_item_tuple_and_item_data_object_equals(
                query_item, prepare_compare_item_data
            )
