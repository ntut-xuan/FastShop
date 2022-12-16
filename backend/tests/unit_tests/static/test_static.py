from __future__ import annotations

from base64 import b64decode
from dataclasses import dataclass
from http import HTTPStatus
from typing import TYPE_CHECKING, cast
from uuid import UUID

import pytest

from response_message import (
    ABSENT_IMAGE_WITH_SPECIFIC_UUID,
    INVALID_UUID,
)
from static.util import (
    get_image_byte_data_from_base64_content,
    get_image_byte,
    has_image_with_specific_uuid,
)

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient
    from werkzeug.test import TestResponse


@dataclass
class SomeImage:
    uuid: str
    base64_byte_content: bytes


@pytest.fixture
def logged_in_client(client: FlaskClient) -> FlaskClient:
    client.post("/login", json={"e-mail": "test@email.com", "password": "test"})
    return client


@pytest.fixture
def add_image(logged_in_client: FlaskClient) -> SomeImage:
    """Adds an image with base64 data `ZG9lc19ub3RfbWF0dGVy` into the static folder.

    Returns:
        SomeImage: Contains the uuid and the byte data of the image.
    """
    base64_image_content: str = "data:image/png;base64,ZG9lc19ub3RfbWF0dGVy"  # The base64 encode result of "does_not_matter"
    response: TestResponse = logged_in_client.post(
        "/static/images", data=base64_image_content, content_type="text/plain"
    )

    # ignore type because response.json returns "Any | None" but we're sure it's a string
    uuid: str = response.json["uuid"]  # type: ignore[index]
    image_byte_data: bytes = get_image_byte_data_from_base64_content(
        base64_image_content
    )
    return SomeImage(uuid, image_byte_data)


@pytest.fixture
def some_absent_uuid() -> UUID:
    """Returns a UUID object of `15cb8517-32d6-436f-b8dc-1e1d2a9e8163`.

    Because the route taking UUID path as a parameter will check whether the UUID is valid or not,
    we want to unitary the absent UUID while testing.
    We assume `15cb8517-32d6-436f-b8dc-1e1d2a9e8163.png` does not exist in the static folder.
    """
    return UUID("15cb8517-32d6-436f-b8dc-1e1d2a9e8163")


class TestImageRoute:
    def test_upload_image_should_return_401_if_user_not_logged_in(
        self, client: FlaskClient
    ) -> None:
        content: str = "data:image/png;base64,..."

        response: TestResponse = client.post(
            "/static/images", data=content, content_type="text/plain"
        )

        assert response.status_code == 401

    def test_upload_image_should_store_base64_to_static_file(
        self, app: Flask, logged_in_client: FlaskClient
    ) -> None:
        base64_image_content = (
            "ZG9lc19ub3RfbWF0dGVy"  # The base64 encode result of "does_not_matter"
        )
        content: str = f"data:image/png;base64,{base64_image_content}"
        with app.app_context():

            response: TestResponse = logged_in_client.post(
                "/static/images", data=content, content_type="text/plain"
            )

            response_data = cast(dict, response.json)
            assert response.status_code == 200
            assert has_image_with_specific_uuid(response_data["uuid"])
            assert get_image_byte(response_data["uuid"]) == b64decode(
                base64_image_content
            )

    def test_upload_image_with_invalid_data_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient
    ) -> None:
        invalid_data: str = "____________=="
        content: str = f"data:image/png;base64,{invalid_data}"

        response: TestResponse = logged_in_client.post(
            "/static/images", data=content, content_type="text/plain"
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_get_image_with_invalid_uuid_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient
    ) -> None:
        invalid_uuid: str = "________-____-____-____-____________"

        # [Act] Try get the image with invalid UUID by GET method.
        response: TestResponse = logged_in_client.get(f"/static/images/{invalid_uuid}")

        # [Assert] It should return HTTP status code FORBIDDEN.
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_get_image_with_valid_uuid_should_return_image(
        self, logged_in_client: FlaskClient, add_image: SomeImage
    ) -> None:
        # [Arrange] Add the image and fetch its uuid and content.
        uuid: str = add_image.uuid
        image_byte_data: bytes = add_image.base64_byte_content

        # [Act] Get the image by GET method.
        response: TestResponse = logged_in_client.get(f"/static/images/{uuid}")

        # [Assert]
        # It should return the image bytes data by mimetype image/png,
        # so basically we can compare the bytes of base64_image_byte_data to the response data (bytes).
        response_image_byte_data: bytes = response.data
        assert image_byte_data == response_image_byte_data

    def test_get_image_with_absent_uuid_should_return_http_status_code_not_found(
        self, logged_in_client: FlaskClient, some_absent_uuid: UUID
    ) -> None:
        # [Act] Get the image with absent UUID by GET method.
        response: TestResponse = logged_in_client.get(
            f"/static/images/{some_absent_uuid}"
        )

        # [Assert] It should return HTTP status code NOT_FOUND.
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_modify_image_should_return_http_status_code_unauthorized_if_not_logged_in(
        self, client: FlaskClient
    ) -> None:
        # [Act] Try modify the image by PUT method without login.
        response: TestResponse = client.put("/static/images/DOES-NOT-MATTER-HERE")

        # [Assert] It should return HTTP status code UNAUTHORIZED.
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_modify_image_with_absent_uuid_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, some_absent_uuid: UUID
    ) -> None:
        # [Act] Try modify the image with absent UUID by PUT method.
        response: TestResponse = logged_in_client.put(
            f"/static/images/{some_absent_uuid}"
        )

        # [Assert] It should return HTTP status code FORBIDDEN.
        response_data = cast(dict, response.json)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_data["message"] == ABSENT_IMAGE_WITH_SPECIFIC_UUID

    def test_modify_image_with_invalid_uuid_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient
    ) -> None:
        invalid_uuid: str = "________-____-____-____-____________"

        # [Act] Try modify the image with invalid UUID by PUT method.
        response: TestResponse = logged_in_client.put(f"/static/images/{invalid_uuid}")

        # [Assert] It should return HTTP status code FORBIDDEN.
        response_data = cast(dict, response.json)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_data["message"] == INVALID_UUID

    def test_modify_image_with_invalid_image_content_should_return_http_status_code_bad_request(
        self, logged_in_client: FlaskClient, add_image: SomeImage
    ) -> None:
        # [Arrange] Add the image and fetch its uuid and content.
        uuid: str = add_image.uuid
        image_base64_content: str = "data:image/png;base64,____________=="

        # [Act] Try modify the image with invalid base64 content by PUT method.
        response: TestResponse = logged_in_client.put(
            f"/static/images/{uuid}",
            data=image_base64_content,
            content_type="text/plain",
        )

        # [Assert] It should return HTTP status code BAD_REQUEST.
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_modify_image_with_exist_uuid_should_modify_successfully(
        self, app: Flask, logged_in_client: FlaskClient, add_image: SomeImage
    ) -> None:
        # [Arrange] Add the image and fetch its uuid and content.
        # It needs app_context to know where the static folder is from config.
        uuid: str = add_image.uuid
        new_image_base64_content: str = "data:image/png;base64,eWV0X2Fub3RoZXJfZG9lc19ub3RfbWF0dGVy"  # The base64 encode of yet_another_does_not_matter
        new_image_byte_data: bytes = get_image_byte_data_from_base64_content(
            new_image_base64_content
        )
        with app.app_context():

            # [Act] Replace the existing image with the new image.
            response: TestResponse = logged_in_client.put(
                f"/static/images/{uuid}",
                data=new_image_base64_content,
                content_type="text/plain",
            )

            # [Assert] It should modify successfully.
            assert response.status_code == HTTPStatus.OK
            assert get_image_byte(uuid) == new_image_byte_data

    def test_delete_image_should_return_http_status_code_unauthorized_if_not_logged_in(
        self, client: FlaskClient
    ) -> None:
        # [Act] Delete the image by DELETE method without logging in.
        response: TestResponse = client.delete("/static/images/does-not-matter")

        # [Assert] It should return HTTP status code UNAUTHORIZED.
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_delete_image_with_invalid_uuid_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient
    ) -> None:
        invalid_uuid: str = "________-____-____-____-____________"
        # [Act] Delete the image with invalid UUID by DELETE method.
        response: TestResponse = logged_in_client.delete(
            f"/static/images/{invalid_uuid}"
        )

        # [Assert] It should return HTTP status code FORBIDDEN.
        response_data = cast(dict, response.json)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_data["message"] == INVALID_UUID

    def test_delete_image_with_absent_uuid_should_return_http_status_code_forbidden(
        self, logged_in_client: FlaskClient, some_absent_uuid: UUID
    ) -> None:
        # [Act] Delete the image with absent UUID by DELETE method.
        response: TestResponse = logged_in_client.delete(
            f"/static/images/{some_absent_uuid}"
        )

        # [Assert] It should return HTTP status code FORBIDDEN.
        response_data = cast(dict, response.json)
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_data["message"] == ABSENT_IMAGE_WITH_SPECIFIC_UUID

    def test_delete_image_with_exist_uuid_should_delete_successfully(
        self, app: Flask, logged_in_client: FlaskClient, add_image: SomeImage
    ) -> None:
        # [Arrange] Add the image and fetch its uuid.
        # It needs app_context to know where the static folder is from config.
        uuid: str = add_image.uuid
        with app.app_context():

            # [Act] Delete the existing image.
            response: TestResponse = logged_in_client.delete(f"/static/images/{uuid}")

            # [Assert] It should delete successfully.
            assert response.status_code == HTTPStatus.OK
            assert not has_image_with_specific_uuid(uuid)
