from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from database import db
from order.util import has_count_larger_than_available
from models import Item

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


def test_has_count_larger_than_available_with_counts_smaller_than_available_should_return_false(
    app: Flask,
) -> None:
    item_ids_and_counts: list[dict[str, int]] = [
        {"item_id": 1, "count": 3},
        {"item_id": 2, "count": 1},
    ]

    with app.app_context():
        assert not has_count_larger_than_available(item_ids_and_counts)


def test_has_count_larger_than_available_with_count_larger_than_available_should_return_true(
    app: Flask,
) -> None:
    count_larger_than_available: int = 100
    item_ids_and_counts: list[dict[str, int]] = [
        {"item_id": 1, "count": 3},
        {"item_id": 2, "count": count_larger_than_available},
    ]

    with app.app_context():
        assert has_count_larger_than_available(item_ids_and_counts)
