from __future__ import annotations

from typing import Any, TYPE_CHECKING

import pytest
from pydantic.error_wrappers import ValidationError
from sqlalchemy import func

from database import db
from item.util import ItemData, TagData, add_item_data, covert_item_object, convert_tags_object_list
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

def is_item_tuple_and_item_data_object_equals(item: tuple[Any], item_data: ItemData) -> bool:
    return (
        item[1] == item_data.name and # Column 2 is name
        item[2] == item_data.count and # Column 3 is count
        item[3] == item_data.price.original and # Column 4 is original price
        item[4] == item_data.price.discount and # Column 5 is discount price
        item[5] == item_data.avatar # Column 6 is avatar
    )


@pytest.fixture
def item_data(item_data_dict: dict[str, Any]) -> ItemData:
    return covert_item_object(item_data_dict)


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

    def test_no_discount_price_dict_should_ok(self, item_data_dict: dict[str, Any]):
        del item_data_dict["price"]["discount"]

        covert_item_object(item_data_dict)


def test_tags_dict_list_convert_to_tags_object_list_should_ok(
    item_data_dict: dict[str, Any]
):
    tags_object_list = convert_tags_object_list(item_data_dict["tags"])

    assert isinstance(tags_object_list, list)
    for object in tags_object_list:
        assert isinstance(object, TagData)


def test_add_item_by_id_should_ok(app: Flask, item_data: ItemData):
    count_item_stmt: Select = db.select([func.count(Item.id)]).select_from(Item).where(Item.id == id)
    item_data_select_stmt: Select = db.select(['*']).select_from(Item).where(Item.id == id)
    with app.app_context():
    
        id = add_item_data(item_data)
        count: int = db.session.execute(count_item_stmt).scalar_one()
        item: tuple = db.session.execute(item_data_select_stmt).one()
        
        assert count == 1
        assert is_item_tuple_and_item_data_object_equals(item, item_data)
        