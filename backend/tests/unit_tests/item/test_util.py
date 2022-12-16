from __future__ import annotations

from typing import Any

import pytest
from pydantic.error_wrappers import ValidationError

from item.util import ItemData, TagData, covert_item_object, convert_tags_object_list


@pytest.fixture
def item_data_dict() -> dict:
    return {
        "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
        "count": 44,
        "name": "Entropy",
        "price": {"discount": 43210, "original": 48763},
        "tags": [{"id": 33, "name": "dian"}],
    }


class TestGetItemFromItemDataDict:
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
