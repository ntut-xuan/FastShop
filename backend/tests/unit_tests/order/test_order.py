from __future__ import annotations

from typing import TYPE_CHECKING, Any

from database import db
from models import Order

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


class TestPostOrdersRoute:
    def test_with_correct_payload_should_add_to_database(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        payload: dict[str, Any] = {
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

        response: TestResponse = logged_in_client.post("/orders", json=payload)

        response_payload: dict[str, Any] | None = response.json
        assert response_payload is not None
        order_id: int = response_payload["id"]
        with app.app_context():
            order: Order | None = db.session.get(Order, order_id)  # type: ignore[attr-defined]
            assert order is not None
            assert order.user_id == 1
            assert order.date == payload["date"]
            assert order.note == payload["note"]
            assert order.delivery_email == payload["delivery_info"]["email"]
            assert order.delivery_firstname == payload["delivery_info"]["firstname"]
            assert order.delivery_lastname == payload["delivery_info"]["lastname"]
            assert order.delivery_address == payload["delivery_info"]["address"]
            assert order.phone == payload["delivery_info"]["phone_number"]
