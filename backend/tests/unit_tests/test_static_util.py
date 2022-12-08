from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from static.exception import FileNotExistError
from static.util import (
    is_image_with_specific_id_exist,
    delete_image,
    put_image,
)

if TYPE_CHECKING:
    from flask import Flask


@pytest.fixture
def image_object_fixture() -> tuple:
    some_image_base64_content = "data:image/png;base64,somecontent"
    some_image_uuid = "c11d5bcf-f529-4318-904d-4bc8b8d7f68a"
    yield (some_image_base64_content, some_image_uuid)


class TestStorageImage:
    def test_put_image_by_absent_uuid_should_create_image(
        self, app: Flask, image_object_fixture: tuple
    ) -> None:
        content = image_object_fixture[0]
        uuid = image_object_fixture[1]

        with app.app_context():
            put_image(content, uuid)  # Create image

            assert is_image_with_specific_id_exist(uuid)

            delete_image(uuid)  # Teardown

    def test_delete_image_by_absent_uuid_should_throw_exceptions(
        self, app: Flask
    ) -> None:
        with pytest.raises(FileNotExistError):
            with app.app_context():
                delete_image("a-b-c-d-eeeee")

    def test_delete_image_by_exist_uuid_should_delete_image(
        self, app: Flask, image_object_fixture: tuple
    ) -> None:
        content = image_object_fixture[0]
        uuid = image_object_fixture[1]

        with app.app_context():
            put_image(content, uuid)  # Create image
            delete_image(uuid)  # Delete image

            assert not is_image_with_specific_id_exist(uuid)
