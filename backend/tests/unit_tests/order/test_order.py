from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from database import db
from models import DeliveryStatus, Order, OrderStatus

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


class TestPostOrdersRoute:
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
