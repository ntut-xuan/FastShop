from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Final

import pytest

from database import db
from models import DeliveryStatus, Item, ItemOfOrder, Order, OrderStatus
from response_message import INVALID_DATA, WRONG_DATA_FORMAT

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

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        response: TestResponse = client.post("/orders", json=order_payload)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    @pytest.mark.parametrize(argnames="unavailable_item_count", argvalues=(-1, 100))
    def test_with_unavailable_item_count_should_respond_forbidden_with_message(
        self,
        logged_in_client: FlaskClient,
        order_payload: dict[str, Any],
        unavailable_item_count: int,
    ) -> None:
        item_id_and_count: dict[str, int] = {"id": 1, "count": unavailable_item_count}
        order_payload["items"] = [item_id_and_count]

        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "Exists unavailable item in the order."
        }

    def test_with_non_existent_item_id_should_respond_forbidden_with_message(
        self, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        non_existent_item_id: Final = 100
        item_id_and_count: dict[str, int] = {"id": non_existent_item_id, "count": 1}
        order_payload["items"] = [item_id_and_count]

        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "Exists unavailable item in the order."
        }

    def test_when_missing_key_should_respond_bad_request_with_message(
        self, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        del order_payload["date"]

        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.get_json(silent=True) == {"message": WRONG_DATA_FORMAT}

    def test_when_missing_payload_should_respond_bad_request_with_message(
        self, logged_in_client: FlaskClient
    ) -> None:
        response: TestResponse = logged_in_client.post("/orders")

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.get_json(silent=True) == {"message": WRONG_DATA_FORMAT}

    def test_with_extra_key_should_respond_OK(
        self, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        order_payload["extra_key"] = "extra"

        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        assert response.status_code == HTTPStatus.OK

    def test_when_payload_has_incorrect_data_type_should_respond_unprocessable_entity_with_message(
        self, logged_in_client: FlaskClient, order_payload: dict[str, Any]
    ) -> None:
        order_payload["date"] = str(order_payload["date"])

        response: TestResponse = logged_in_client.post("/orders", json=order_payload)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.get_json(silent=True) == {"message": INVALID_DATA}


class TestDeleteOrdersByIdRoute:
    @pytest.fixture(autouse=True)
    def insert_test_data(self, app: Flask) -> None:
        with app.app_context():
            # fmt: off
            db.session.add(Item(id=1, name="apple", count=10, description="This is an apple.", original=30, discount=25, avatar="xx-S0m3-aVA7aR-0f-a991e-xx"))
            db.session.add(Order(order_id=1, user_id=1, date=1672737308, order_status=OrderStatus.OK, delivery_status=DeliveryStatus.PENDING, delivery_address="somewhere", note="some note", phone="0123456789"))
            db.session.flush()  # flush first so ItemOfOrder has the foreign key
            db.session.add(ItemOfOrder(order_id=1, item_id=1, count=2))
            # fmt: on
            db.session.commit()

    def test_with_existing_order_id_should_response_ok_with_message(
        self, logged_in_client: FlaskClient
    ) -> None:
        existing_order_id: Final = 1

        response: TestResponse = logged_in_client.delete(f"/orders/{existing_order_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == {"message": "OK"}

    def test_with_existing_order_id_should_delete_the_order_from_database(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        existing_order_id: Final = 1

        logged_in_client.delete(f"/orders/{existing_order_id}")

        with app.app_context():
            order: Order | None = db.session.get(Order, existing_order_id)  # type: ignore[attr-defined]
            assert order is None

    def test_with_existing_order_id_should_delete_the_item_of_order_from_database(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        existing_order_id: Final = 1

        logged_in_client.delete(f"/orders/{existing_order_id}")

        with app.app_context():
            items_of_order: list[ItemOfOrder] = (
                db.session.execute(
                    db.select(ItemOfOrder).where(
                        ItemOfOrder.order_id == existing_order_id
                    )
                )
                .scalars()
                .all()
            )
            assert len(items_of_order) == 0

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.delete("/orders/1")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    @pytest.mark.parametrize(
        argnames="undeletable_delivery_status",
        argvalues=(DeliveryStatus.DELIVERING, DeliveryStatus.DELIVERED),
    )
    def test_with_order_in_undeletable_delivery_status_should_respond_forbidden_with_message(
        self,
        app: Flask,
        logged_in_client: FlaskClient,
        undeletable_delivery_status: DeliveryStatus,
    ) -> None:
        with app.app_context():
            db.session.add(
                Order(
                    order_id=2,
                    user_id=1,
                    date=1672737308,
                    order_status=OrderStatus.OK,
                    delivery_status=undeletable_delivery_status,
                    delivery_address="somewhere",
                    note="some note",
                    phone="0123456789",
                )
            )
            db.session.flush()  # flush first so ItemOfOrder has the foreign key
            db.session.add(ItemOfOrder(order_id=2, item_id=1, count=2))
            db.session.commit()

        response: TestResponse = logged_in_client.delete(f"/orders/2")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The order is not possible to be deleted since the order is now delivering or has been delivered."
        }


class TestGetOrdersByIdRoute:
    @pytest.fixture(autouse=True)
    def insert_test_data(self, app: Flask) -> None:
        with app.app_context():
            db.session.add(Item(id=1, name="apple", count=10, description="This is an apple.", original=30, discount=25, avatar="xx-S0m3-aVA7aR-0f-a991e-xx"))  # fmt: skip
            db.session.add(Item(id=2, name="tilapia", count=5, description="This is an tilapia.", original=50, discount=45, avatar="xx-S0m3-aVA7aR-0f-ti1a9iA-xx"))  # fmt: skip
            db.session.add(
                Order(
                    order_id=1,
                    user_id=1,
                    date=1672737308,
                    order_status=OrderStatus.OK,
                    delivery_status=DeliveryStatus.PENDING,
                    delivery_address="somewhere",
                    note="some note",
                    phone="0123456789",
                )
            )
            db.session.flush()  # flush first so ItemOfOrder has the foreign key
            db.session.add(ItemOfOrder(order_id=1, item_id=1, count=2))
            db.session.add(ItemOfOrder(order_id=1, item_id=2, count=1))
            db.session.commit()

    def test_with_existing_order_id_should_return_the_order(
        self, logged_in_client: FlaskClient
    ) -> None:
        existing_order_id: Final = 1
        expected_payload: dict[str, Any] = {
            "delivery_status": "PENDING",
            "detail": {
                "date": 1672737308,
                "delivery_info": {
                    "address": "somewhere",
                    "email": "test@email.com",
                    "firstname": "Han-Xuan",
                    "lastname": "Huang",
                    "phone_number": "0123456789",
                },
                "items": [{"count": 2, "id": 1}, {"count": 1, "id": 2}],
                "note": "some note",
            },
            "id": 1,
            "status": "OK",
        }

        response: TestResponse = logged_in_client.get(f"/orders/{existing_order_id}")

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == expected_payload

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.get("/orders/1")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    def test_with_absent_order_id_should_respond_forbidden_with_message(
        self, logged_in_client: FlaskClient
    ) -> None:
        absent_order_id: Final = 100

        response: TestResponse = logged_in_client.get(f"/orders/{absent_order_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of the order is absent."
        }
