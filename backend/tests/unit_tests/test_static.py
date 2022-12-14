from __future__ import annotations

from base64 import b64decode
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

import pytest
from http import HTTPStatus

from static.util import (
    get_image_byte_data_from_base64_content,
    get_image_byte_from_existing_file,
    has_image_with_specific_id,
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
def login_client(client: FlaskClient) -> None:
    client.post(
        "/login",
        json={
            "e-mail": "test@email.com",
            "password": "test",
        },
    )
    return client


@pytest.fixture
def add_image(login_client: FlaskClient) -> SomeImage:
    base64_image_content: str = "data:image/png;base64,ZG9lc19ub3RfbWF0dGVy"  # The base64 encode result of "does_not_matter"
    image_byte_data: bytes = get_image_byte_data_from_base64_content(
        base64_image_content
    )
    response: TestResponse = login_client.post(
        "/static/images", data=base64_image_content, content_type="text/plain"
    )
    # Type: ignore because response.json return Any | None, so it will return any random shit to us.
    uuid: str = response.json["uuid"]  # type: ignore
    return SomeImage(uuid, image_byte_data)


class TestImageRoute:
    def test_upload_image_should_return_401_if_user_not_login(
        self, client: FlaskClient
    ):
        content: str = "data:image/png;base64,..."

        response: TestResponse = client.post(
            "/static/images", data=content, content_type="text/plain"
        )

        assert response.status_code == 401

    def test_upload_image_should_store_base64_to_static_file_path(
        self, app: Flask, login_client: FlaskClient
    ):
        base64_image_content = (
            "ZG9lc19ub3RfbWF0dGVy"  # The base64 encode result of "does_not_matter"
        )
        content: str = "data:image/png;base64," + base64_image_content
        with app.app_context():

            response: TestResponse = login_client.post(
                "/static/images", data=content, content_type="text/plain"
            )

            data_dict: dict[str, Any] = response.json  # type: ignore
            assert response.status_code == 200
            assert has_image_with_specific_id(data_dict["uuid"])
            assert get_image_byte_from_existing_file(data_dict["uuid"]) == b64decode(
                base64_image_content
            )

    def test_upload_image_with_invalid_content_should_return_http_status_code_bad_request(
        self, login_client: FlaskClient
    ):
        content: str = "data:image/png;base64,____________=="

        response: TestResponse = login_client.post(
            "/static/images", data=content, content_type="text/plain"
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_get_image_with_valid_uuid_should_return_image(
        self, login_client: FlaskClient, add_image: SomeImage
    ):
        # [Arrange] Add the image and fetch the uuid.
        uuid = add_image.uuid
        image_byte_data = add_image.base64_byte_content

        # [Act] Get the image by GET method
        response: TestResponse = login_client.get(f"/static/images/{uuid}")

        # [Assert]
        # It should return the image bytes data by mimetype image/png
        # So basically we can compare the bytes of base64_image_byte_data to the response data (bytes)
        response_image_byte_data: bytes = response.data
        assert image_byte_data == response_image_byte_data

    def test_get_image_with_absent_uuid_should_http_status_code_not_found(
        self, login_client: FlaskClient
    ):
        # [Act] Get the image with absent UUID by GET method.
        response: TestResponse = login_client.get("/static/images/DOES-NOT-MATTER-HERE")

        # [Assert] It should be return HTTP status code NOT_FOUND.
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_modify_image_should_return_http_status_code_unauthorized_if_not_login(
        self, client: FlaskClient
    ):
        # [Act] Try modify the image by PUT method without login.
        response: TestResponse = client.put("/static/images/DOES-NOT-MATTER-HERE")

        # [Assert] It should be return HTTP status code UNAUTHORIZED.
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_modify_image_with_absent_uuid_should_return_http_status_code_forbidden(
        self, login_client: FlaskClient
    ):
        # [Act] Try modify the image with absent UUID by PUT method.
        response: TestResponse = login_client.put("/static/images/DOES-NOT-MATTER-HERE")

        # [Assert] It should be return HTTP status code FORBIDDEN.
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_modify_image_with_invalid_image_content_should_return_http_status_code_bad_request(
        self, login_client: FlaskClient, add_image: SomeImage
    ):
        # [Arrange] Add the image and fetch the uuid. Modify the image with invalid image base64 content.
        uuid: str = add_image.uuid
        image_base64_content: str = "data:image/png;base64,____________=="

        # [Act] Try modify the image with invalid base64 content by PUT method
        response: TestResponse = login_client.put(
            f"/static/images/{uuid}",
            data=image_base64_content,
            content_type="text/plain",
        )

        # [Assert] It should return HTTP status code BAD_REQUEST
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_modify_image_with_exist_uuid_should_modify_successfully(
        self, app: Flask, login_client: FlaskClient, add_image: SomeImage
    ):
        # [Arrange] Add the image and fetch the uuid.
        # It will use app_context in Flask app because get_image_byte_from_existing_file.
        uuid: str = add_image.uuid
        new_image_base64_content: str = "data:image/png;base64,eWV0X2Fub3RoZXJfZG9lc19ub3RfbWF0dGVy"  # The base64 encode of yet_another_does_not_matter
        new_image_byte_data: bytes = get_image_byte_data_from_base64_content(
            new_image_base64_content
        )
        with app.app_context():

            # [Act] Replace the existing image to the new image
            response: TestResponse = login_client.put(
                f"/static/images/{uuid}",
                data=new_image_base64_content,
                content_type="text/plain",
            )

            # [Assert] It should be modify successfully
            assert response.status_code == HTTPStatus.OK
            assert get_image_byte_from_existing_file(uuid) == new_image_byte_data

    def test_delete_image_should_return_http_status_code_unauthorized_if_not_login(
        self, client: FlaskClient
    ):
        # [Act] Delete the image by DELETE method without login
        response: TestResponse = client.delete("/static/images/DOES-NOT-MATTER")

        # [Assert] It should return HTTP status code UNAUTHORIZED
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_delete_image_with_absent_uuid_should_return_http_status_code_forbidden(
        self, login_client: FlaskClient
    ):
        # [Act] Delete the image with absend UUID by DELETE method.
        response: TestResponse = login_client.delete("/static/images/DOES-NOT-MATTER")

        # [Assert] It should return HTTP status code FORBIDDEN.
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_delete_image_with_exist_uuid_should_delete_successfully(
        self, app: Flask, login_client: FlaskClient, add_image: SomeImage
    ):
        # [Arrange] Add the image and fetch the uuid.
        # It will use app_context in Flask app because has_image_with_specific_id
        uuid: str = add_image.uuid
        with app.app_context():

            # [Act] Delete the existing image.
            response: TestResponse = login_client.delete(f"/static/images/{uuid}")

            # [Assert] It should delete successfully.
            assert response.status_code == HTTPStatus.OK
            assert not has_image_with_specific_id(uuid)
