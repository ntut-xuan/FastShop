from __future__ import annotations

from typing import Any

import pytest
from pydantic.error_wrappers import ValidationError

from item.util import ItemData, get_item_object_from_item_data_dict


class TestGetItemFromItemDataDict:
    @pytest.fixture
    def item_data_dict(self) -> dict:
        return {
            "avatar": "f692073a-7ac1-11ed-a1eb-0242ac120002",
            "count": 44,
            "name": "Entropy",
            "price": {"discount": 43210, "original": 48763},
            "tags": [{"id": 33, "name": "dian"}],
        }

    def test_valid_dict_should_return_correct_item_object(
        self, item_data_dict: dict[str, Any]
    ):
        item: ItemData = get_item_object_from_item_data_dict(item_data_dict)

        assert item.avatar == "f692073a-7ac1-11ed-a1eb-0242ac120002"
        assert item.count == 44
        assert item.name == "Entropy"
        assert item.price.discount == 43210
        assert item.price.original == 48763
        assert item.tags[0].id == 33
        assert item.tags[0].name == "dian"

    def test_incorrect_format_dict_should_raise_missing_fields_error(self):
        with pytest.raises(KeyError):
            get_item_object_from_item_data_dict({"wrong_column": "wrong_value"})

    def test_invalid_data_dict_should_raise_error(self, item_data_dict: dict[str, Any]):
        item_data_dict[
            "count"
        ] = "5"  # Since count require integer-type data, it should cause error.

        with pytest.raises(ValidationError):
            get_item_object_from_item_data_dict(item_data_dict)

    def test_no_tags_dict_should_ok(self, item_data_dict: dict[str, Any]):
        del item_data_dict["tags"]

        get_item_object_from_item_data_dict(item_data_dict)

    def test_no_discount_price_dict_should_ok(self, item_data_dict: dict[str, Any]):
        del item_data_dict["price"]["discount"]

        get_item_object_from_item_data_dict(item_data_dict)
