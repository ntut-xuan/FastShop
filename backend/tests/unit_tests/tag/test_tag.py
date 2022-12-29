from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, cast

import pytest

from database import db
from models import Item, Tag, TagOfItem
from response_message import INVALID_DATA, WRONG_DATA_FORMAT

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@pytest.fixture
def test_tags(app: Flask) -> list[dict[str, Any]]:
    """Inserts some tags into the database.

    Returns:
       A list of dicts contains the attributes of the inserted tags.
    """
    tags: list[dict[str, Any]] = [
        {"id": 1, "name": "seafood"},
        {"id": 2, "name": "fruit"},
        {"id": 3, "name": "solid food"},
    ]
    with app.app_context():
        db.session.execute(db.insert(Tag), tags)
        db.session.commit()
    return tags


class TestGetTagsRoute:
    def test_when_no_existing_tag_should_respond_count_zero(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.get("/tags")

        data = cast(dict, response.json)
        count: int = data["count"]
        assert count == 0

    def test_when_tag_exist_should_respond_all_existing_tags(
        self, client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        response: TestResponse = client.get("/tags")

        assert response.json is not None
        data: dict[str, Any] = response.json
        assert data["count"] == len(test_tags)
        responded_tags: list[dict[str, Any]] = data["tags"]
        for tag in responded_tags:
            assert tag in test_tags


class TestPostTagsRoute:
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
            ).one_or_none()
        assert tag is not None

    @pytest.mark.parametrize(
        argnames="payload",
        argvalues=(
            None,  # missing payload
            {"should be name": "xxx"},  # missing key "name"
        ),
    )
    def test_with_wrong_data_format_should_respond_bad_request_with_message(
        self, logged_in_client: FlaskClient, payload: dict[str, Any] | None
    ) -> None:
        response: TestResponse = logged_in_client.post("/tags", json=payload)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.get_json(silent=True) == {"message": WRONG_DATA_FORMAT}

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient
    ) -> None:
        response: TestResponse = client.post("/tags", json={"name": "some tag"})

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    def test_with_existing_tag_should_respond_forbidden_with_message(
        self, logged_in_client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]

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
    def test_with_existing_tag_id_should_return_the_tag(
        self, client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]

        response: TestResponse = client.get(f"/tags/{existing_tag['id']}")

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == existing_tag

    def test_with_absent_tag_id_should_respond_forbidden_with_message(
        self, client: FlaskClient
    ) -> None:
        absent_tag_id = 100

        response: TestResponse = client.get(f"/tags/{absent_tag_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of tag is absent."
        }


class TestDeleteTagsByIdRoute:
    def test_with_existing_tag_id_should_response_ok_with_message(
        self, logged_in_client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]

        response: TestResponse = logged_in_client.delete(f"/tags/{existing_tag['id']}")

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == {"message": "OK"}

    def test_with_existing_tag_id_should_delete_the_tag(
        self, app: Flask, logged_in_client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        target: dict[str, Any] = test_tags[0]

        logged_in_client.delete(f"/tags/{target['id']}")

        with app.app_context():
            tag: Tag | None = db.session.get(Tag, target["id"])  # type: ignore[attr-defined]
            assert tag is None

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]

        response: TestResponse = client.delete(f"/tags/{existing_tag['id']}")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    def test_with_absent_tag_id_should_respond_forbidden_with_message(
        self, logged_in_client: FlaskClient
    ) -> None:
        absent_tag_id = 100

        response: TestResponse = logged_in_client.delete(f"/tags/{absent_tag_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of tag is absent."
        }


class TestPutTagsByIdRoute:
    def test_with_existing_tag_id_should_update_the_tag(
        self, app: Flask, logged_in_client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        new_tag_name = "new tag name"
        existing_tag: dict[str, Any] = test_tags[0]

        logged_in_client.put(f"/tags/{existing_tag['id']}", json={"name": new_tag_name})

        with app.app_context():
            tag: Tag | None = db.session.get(Tag, existing_tag["id"])  # type: ignore[attr-defined]
            assert tag is not None
            assert tag.name == new_tag_name

    def test_with_existing_tag_id_should_response_ok_with_message(
        self, logged_in_client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        new_tag_name = "new tag name"
        existing_tag: dict[str, Any] = test_tags[0]

        response: TestResponse = logged_in_client.put(
            f"/tags/{existing_tag['id']}", json={"name": new_tag_name}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.get_json(silent=True) == {"message": "OK"}

    def test_when_not_logged_in_should_respond_unauthorized_with_message(
        self, client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]

        response: TestResponse = client.put(
            f"/tags/{existing_tag['id']}", json={"name": "some tag name"}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.get_json(silent=True) == {"message": "Unauthorized."}

    @pytest.mark.parametrize(
        argnames="payload",
        argvalues=(
            None,  # missing payload
            {"should be name": "xxx"},  # missing key "name"
        ),
    )
    def test_with_wrong_data_format_should_respond_bad_request_with_message(
        self,
        logged_in_client: FlaskClient,
        test_tags: list[dict[str, Any]],
        payload: dict[str, Any] | None,
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]

        response: TestResponse = logged_in_client.put(
            f"/tags/{existing_tag['id']}", json=payload
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.get_json(silent=True) == {"message": WRONG_DATA_FORMAT}

    def test_with_absent_tag_id_should_respond_forbidden_with_message(
        self, logged_in_client: FlaskClient
    ) -> None:
        absent_tag_id = 100

        response: TestResponse = logged_in_client.put(f"/tags/{absent_tag_id}")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of tag is absent."
        }

    def test_with_wrong_value_type_should_respond_unprocessable_entity_with_message(
        self, logged_in_client: FlaskClient, test_tags: list[dict[str, Any]]
    ) -> None:
        existing_tag: dict[str, Any] = test_tags[0]
        tag_name_in_int_type = 0

        response: TestResponse = logged_in_client.put(
            f"/tags/{existing_tag['id']}", json={"name": tag_name_in_int_type}
        )

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response.get_json(silent=True) == {"message": INVALID_DATA}


class TestGetItemsByIdOfTagRoute:
    @pytest.fixture(autouse=True)
    def insert_test_data(self, app: Flask) -> None:
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
            db.session.execute(
                db.insert(Tag),
                [
                    {"id": 1, "name": "fruit"},
                    {"id": 2, "name": "fish"},
                    {"id": 3, "name": "grocery"},
                ],
            )
            db.session.execute(
                db.insert(TagOfItem),
                [
                    {"item_id": 1, "tag_id": 1},
                    {"item_id": 2, "tag_id": 2},
                    {"item_id": 1, "tag_id": 3},
                    {"item_id": 2, "tag_id": 3},
                ],
            )
            db.session.commit()

    def test_with_absent_tag_id_should_respond_forbidden_with_message(
        self, client: FlaskClient
    ) -> None:
        absent_tag_id = 100

        response: TestResponse = client.get(f"/tags/{absent_tag_id}/items")

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.get_json(silent=True) == {
            "message": "The specific ID of tag is absent."
        }

    def test_with_tag_id_of_some_items_should_respond_all_items_of_that_tag(
        self, client: FlaskClient
    ) -> None:
        existing_item: dict[str, Any] = {
            "id": 1,
            "name": "apple",
            "count": 10,
            "description": "This is an apple.",
            "original": 30,
            "discount": 25,
            "avatar": "xx-S0m3-aVA7aR-0f-a991e-xx",
        }

        response: TestResponse = client.get(f"/tags/{existing_item['id']}/items")

        assert response.json is not None
        data: dict[str, Any] = response.json
        assert data["count"] == 1
        assert len(data["items"]) == 1
        (responded_item,) = data["items"]
        assert responded_item == existing_item
