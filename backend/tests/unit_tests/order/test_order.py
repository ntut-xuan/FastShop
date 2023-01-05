from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from database import db
from models import DeliveryStatus, Item, ItemOfOrder, Order, OrderStatus

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from sqlalchemy.engine.row import Row
    from werkzeug.test import TestResponse


class TestPostOrdersRoute:
    @pytest.fixture(autouse=True)
    def insert_test_data(self, app: Flask) -> None:
        with app.app_context():
            db.session.add(Item(id=1, name="apple", count=10, description="This is an apple.", original=30, discount=25, avatar="xx-S0m3-aVA7aR-0f-a991e-xx"))  # fmt: skip
            db.session.commit()

    @pytest.fixture
    def order_payload(self) -> dict[str, Any]:
        return {
            "date": 1672737308,
            "delivery_info": {
                "address": "No. 1, Sec. 3, Zhongxiao E. Rd., Da'an Dist., Taipei City 106344 , Taiwan (R.O.C.)",
                "email": "test@test.com",
                "firstname": "Han-Xuan",
                "lastname": "Huang",
                "phone_number": "0921474836",
            },
            "items": [],
            "note": "No Iansui",
        }

    def test_with_correct_payload_should_add_to_database(
        self, app: Flask, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        order_id: int = response_payload["id"]
        with app.app_context():
            order: Order | None = db.session.get(Order, order_id)  # type: ignore[attr-defined]
            assert order is not None
            assert order.user_id == 1
            assert order.date == order_payload["date"]
            assert order.note == order_payload["note"]
            assert order.delivery_email == order_payload["delivery_info"]["email"]
            assert (
                order.delivery_firstname == order_payload["delivery_info"]["firstname"]
            )
            assert order.delivery_lastname == order_payload["delivery_info"]["lastname"]
            assert order.delivery_address == order_payload["delivery_info"]["address"]
            assert order.phone == order_payload["delivery_info"]["phone_number"]

    def test_with_new_order_should_have_status_of_order_and_delivery_be_checking_and_pending(
        self, app: Flask, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        order_id: int = response_payload["id"]
        with app.app_context():
            order: Order | None = db.session.get(Order, order_id)  # type: ignore[attr-defined]
            assert order is not None
            assert order.order_status is OrderStatus.CHECKING
            assert order.delivery_status is DeliveryStatus.PENDING

    def test_with_correct_payload_should_add_item_of_order_to_database(
        self, app: Flask, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        item_id_and_count: dict[str, int] = {"id": 1, "count": 5}
        order_payload["items"] = [item_id_and_count]

        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        order_id: int = response_payload["id"]
        with app.app_context():
            items: list[Row] = db.session.execute(
                db.select(ItemOfOrder.item_id, ItemOfOrder.count).where(
                    ItemOfOrder.order_id == order_id
                )
            ).all()
            assert len(items) == 1
            item: Row = items[0]
            assert item.item_id == item_id_and_count["id"]
            assert item.count == item_id_and_count["count"]
