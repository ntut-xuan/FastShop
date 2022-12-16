from __future__ import annotations

from http import HTTPStatus
from typing import Any, TYPE_CHECKING, cast

import pytest

from database import db
from models import Tag
from response_message import INVALID_DATA, WRONG_DATA_FORMAT

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@pytest.fixture
def logged_in_client(client: FlaskClient) -> FlaskClient:
    client.post("/login", json={"e-mail": "test@email.com", "password": "test"})
    return client


class TestGetTagsRoute:
    def test_should_return_count_0_if_no_existing_tags(
        self,
        client: FlaskClient,
    ) -> None:
        response: TestResponse = client.get("/tags")

        data = cast(dict, response.json)
        count: int = data["count"]
        assert count == 0

    def test_should_return_all_existing_tags(
        self, app: Flask, client: FlaskClient
    ) -> None:
        tags: list[dict[str, Any]] = [
            {"id": 1, "name": "seafood"},
            {"id": 2, "name": "fruit"},
            {"id": 3, "name": "solid food"},
        ]
        with app.app_context():
            db.session.execute(db.insert(Tag), tags)
            db.session.commit()

        response: TestResponse = client.get("/tags")

        assert response.json is not None
        data: dict[str, Any] = response.json
        assert data["count"] == 3
        responded_tags: list[dict[str, Any]] = data["tags"]
        assert responded_tags[0] in tags
        assert responded_tags[1] in tags
        assert responded_tags[2] in tags


class PostTagsRoute:
    def test_with_non_existent_name_should_add_tag_into_database(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        tag_name: str = "a non-existent tag"

        response: TestResponse = logged_in_client.post("/tags", json={"name": tag_name})

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == {"message": "OK"}
        with app.app_context():
            tag: Tag | None = db.session.execute(
                db.select(Tag).where(Tag.name == tag_name)
            ).scalar_one_or_none()
        assert tag is not None

    @pytest.mark.parametrize(
        argnames=("payload",),
        argvalues=(
            (None,),  # missing payload
            ({"should be name": "xxx"},),  # missing key "name"
        ),
    )
    def test_with_wrong_data_format_should_respond_bad_request_with_message(
        self, logged_in_client: FlaskClient, payload: dict[str, Any] | None
    ) -> None:
        response: TestResponse = logged_in_client.post("/tags", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.get_json(silent=True) == {"message": WRONG_DATA_FORMAT}

    def test_without_logging_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.post("/tags", json={"name": "some tag"})

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    def test_with_existing_tag_should_respond_forbidden_with_message(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        existing_tag: dict[str, Any] = {"id": 1, "name": "black magic"}
        with app.app_context():
            db.session.add(Tag(**existing_tag))
            db.session.commit()

        response: TestResponse = logged_in_client.post("/tags", json=existing_tag)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The tag already exists in the database."
        }

    def test_with_wrong_value_type_should_respond_unprocessable_entity_with_message(
        self, logged_in_client: FlaskClient
    ) -> None:
        tag_name_in_int_type = 0

        response: TestResponse = logged_in_client.post(
            "/tags", json={"name": tag_name_in_int_type}
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.get_json(silent=True) == {"message": INVALID_DATA}


class TestGetTagsByIdRoute:
    def test_should_return_the_tag_if_exist(
        self, app: Flask, client: FlaskClient
    ) -> None:
        existing_tag: dict[str, Any] = {"id": 1, "name": "black magic"}
        with app.app_context():
            db.session.add(Tag(**existing_tag))
            db.session.add(Tag(id=2, name="some other tag"))
            db.session.commit()

        response: TestResponse = client.get(f"/tags/{existing_tag['id']}")

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == existing_tag

    def test_should_respond_forbidden_with_message_if_tag_is_absent(
        self, client: FlaskClient
    ) -> None:
        absent_tag_id = 100

        response: TestResponse = client.get(f"/tags/{absent_tag_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of tag is absent."
        }


class TestDeleteTagsByIdRoute:
    def test_should_response_ok_with_message_if_exist(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        existing_tag: dict[str, Any] = {"id": 1, "name": "black magic"}
        with app.app_context():
            db.session.add(Tag(**existing_tag))
            db.session.add(Tag(id=2, name="some other tag"))
            db.session.commit()

        response: TestResponse = logged_in_client.delete(f"/tags/{existing_tag['id']}")

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == {"message": "OK"}

    def test_should_delete_the_tag_if_exist(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        target: dict[str, Any] = {"id": 1, "name": "black magic"}
        with app.app_context():
            db.session.add(Tag(**target))
            db.session.add(Tag(id=2, name="some other tag"))
            db.session.commit()

        logged_in_client.delete(f"/tags/{target['id']}")

        with app.app_context():
            tag: Tag | None = db.session.execute(
                db.select(Tag).where(Tag.id == target["id"])
            ).scalar()
            assert tag is None

    def test_should_respond_forbidden_with_message_if_tag_is_absent(
        self, client: FlaskClient
    ) -> None:
        absent_tag_id = 100

        response: TestResponse = client.delete(f"/tags/{absent_tag_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of tag is absent."
        }
