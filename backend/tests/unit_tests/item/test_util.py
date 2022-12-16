from __future__ import annotations

from typing import Any, TYPE_CHECKING

import pytest
from pydantic.error_wrappers import ValidationError
from sqlalchemy import func

from database import db
from item.util import (
    ItemData,
    TagData,
    add_item_data,
    covert_item_object,
    convert_tags_object_list,
    has_item_with_specific_id,
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
    compare_result: bool = (
        item[1] == item_data.name  # Column 2 is name
        and item[2] == item_data.count  # Column 3 is count
        and item[3] == item_data.price.original  # Column 4 is original price
        and item[4] == item_data.price.discount  # Column 5 is discount price
        and item[5] == item_data.avatar  # Column 6 is avatar
    )
    return compare_result


@pytest.fixture
def item_data(item_data_dict: dict[str, Any]) -> ItemData:
    converted_item: ItemData = covert_item_object(item_data_dict)
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


def test_tags_dict_list_convert_to_tags_object_list_should_ok(
    item_data_dict: dict[str, Any]
):
    tags_object_list = convert_tags_object_list(item_data_dict["tags"])

    assert isinstance(tags_object_list, list)
    for object in tags_object_list:
        assert isinstance(object, TagData)


def test_add_item_should_ok(app: Flask, item_data: ItemData):
    with app.app_context():

        id = add_item_data(item_data)
        item_data_select_stmt: Select = (
            db.select(["*"]).select_from(Item).where(Item.id == id)
        )
        item: tuple = db.session.execute(item_data_select_stmt).one()

        assert is_item_tuple_and_item_data_object_equals(item, item_data)


def test_check_count_of_non_exist_id_should_return_false(app: Flask):
    with app.app_context():

        assert has_item_with_specific_id(111111) == False


def test_check_count_of_exist_id_should_return_true(app: Flask, place_item: int):
    place_item_id = place_item
    with app.app_context():

        assert has_item_with_specific_id(place_item_id)
