from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from src.database import db
from src.order.util import has_unavailable_count_of_item
from src.models import Item

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
                    "description": "This is an apple.",
                    "original": 30,
                    "discount": 25,
                    "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
                },
                {
                    "id": 2,
                    "name": "tilapia",
                    "count": 3,
                    "description": "This is a tilapia.",
                    "original": 50,
                    "discount": 45,
                    "avatar": "xx-S0m3-aVA7aR-0f-ti1a9iA-xx",
                },
            ],
        )
        db.session.commit()


class TestHasAvailableCountOfItem:
    def test_with_counts_smaller_than_available_should_return_false(
        self, app: Flask
    ) -> None:
        item_ids_and_counts: list[dict[str, int]] = [
            {"id": 1, "count": 3},
            {"id": 2, "count": 1},
        ]

        with app.app_context():
            assert not has_unavailable_count_of_item(item_ids_and_counts)

    def test_with_count_larger_than_available_should_return_true(
        self, app: Flask
    ) -> None:
        count_larger_than_available: int = 100
        item_ids_and_counts: list[dict[str, int]] = [
            {"id": 1, "count": 3},
            {"id": 2, "count": count_larger_than_available},
        ]

        with app.app_context():
            assert has_unavailable_count_of_item(item_ids_and_counts)

    def test_with_negative_count_should_return_true(self, app: Flask) -> None:
        negative_count: int = -1
        item_ids_and_counts: list[dict[str, int]] = [
            {"id": 1, "count": 3},
            {"id": 2, "count": negative_count},
        ]

        with app.app_context():
            assert has_unavailable_count_of_item(item_ids_and_counts)
