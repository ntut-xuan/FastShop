from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from hashlib import sha512

from database import db
from models import Item, ShoppingCart, Tag, TagOfItem, User

if TYPE_CHECKING:
    from click.testing import Result
    from flask import Flask
    from flask.testing import FlaskCliRunner


def test_create_db_command(app: Flask) -> None:
    with app.app_context():
        runner: FlaskCliRunner = app.test_cli_runner()

        result: Result = runner.invoke(args=("create-db",))

    assert result.exit_code == 0
    assert result.output == "Created the database.\n"


def test_query_with_setup_user_data_should_return_expected_value(app: Flask):
    with app.app_context():
        test_user: User = db.session.get(User, 1)  # type: ignore[attr-defined]
        other_user: User = db.session.get(User, 2)  # type: ignore[attr-defined]

        assert test_user.birthday == int(
            datetime(
                year=2002, month=6, day=25, hour=0, minute=0, second=0, microsecond=0
            ).timestamp()
        )
        assert test_user.email == "test@email.com"
        assert test_user.password == sha512("test".encode("utf-8")).hexdigest()
        assert test_user.firstname == "Han-Xuan"
        assert test_user.lastname == "Huang"
        assert test_user.gender == 0

        assert other_user.birthday == int(
            datetime(
                year=2002, month=6, day=25, hour=0, minute=0, second=0, microsecond=0
            ).timestamp()
        )
        assert other_user.email == "other@email.com"
        assert other_user.password == sha512("other".encode("utf-8")).hexdigest()
        assert other_user.firstname == "Xuan"
        assert other_user.lastname == "Uriah"
        assert other_user.gender == 0


def test_query_with_setup_item_data_should_return_expected_value(app: Flask):
    with app.app_context():
        apple: Item = db.session.get(Item, 1)  # type: ignore[attr-defined]
        tilapia: Item = db.session.get(Item, 2)  # type: ignore[attr-defined]

        assert apple.name == "apple"
        assert apple.count == 10
        assert apple.description == "This is an apple."
        assert apple.original == 30
        assert apple.discount == 25
        assert apple.avatar == "xx-S0m3-aVA7aR-0f-a991e-xx"

        assert tilapia.name == "tilapia"
        assert tilapia.count == 3
        assert tilapia.description == "This is a tilapia."
        assert tilapia.original == 50
        assert tilapia.discount == 45
        assert tilapia.avatar == "xx-S0m3-aVA7aR-0f-ti1a9iA-xx"


def test_query_with_setup_tag_data_should_return_expected_value(app: Flask):
    with app.app_context():
        seafood: Tag = db.session.get(Tag, 1)  # type: ignore[attr-defined]
        fruit: Tag = db.session.get(Tag, 2)  # type: ignore[attr-defined]
        grocery: Tag = db.session.get(Tag, 3)  # type: ignore[attr-defined]

        assert seafood.id == 1
        assert seafood.name == "seafood"

        assert fruit.id == 2
        assert fruit.name == "fruit"

        assert grocery.id == 3
        assert grocery.name == "grocery"


def test_query_with_setup_tag_of_item_data_should_return_expected_value(app: Flask):
    with app.app_context():
        item_of_tags: list[TagOfItem] = db.session.query(TagOfItem).all()

        except_result = [
            {"item_id": 1, "tag_id": 1},
            {"item_id": 1, "tag_id": 3},
            {"item_id": 2, "tag_id": 2},
            {"item_id": 2, "tag_id": 3},
        ]

        assert len(item_of_tags) == len(except_result)

        for i in range(len(item_of_tags)):
            assert item_of_tags[i].item_id == except_result[i]["item_id"]
            assert item_of_tags[i].tag_id == except_result[i]["tag_id"]


def test_query_with_setup_shopping_cart_data_should_return_excepted_value(app: Flask):
    with app.app_context():
        item_details: list[ShoppingCart] = db.session.query(ShoppingCart).all()

        except_result = [
            {"user_id": 1, "item_id": 1, "count": 5},
            {"user_id": 1, "item_id": 2, "count": 3},
            {"user_id": 2, "item_id": 2, "count": 3},
        ]

        assert len(item_details) == len(except_result)

        for i in range(len(item_details)):
            assert item_details[i].user_id == except_result[i]["user_id"]
            assert item_details[i].item_id == except_result[i]["item_id"]
            assert item_details[i].count == except_result[i]["count"]
