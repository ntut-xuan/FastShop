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

_some_image_base64_content = "data:image/png;base64,somecontent"
_some_image_uuid = "c11d5bcf-f529-4318-904d-4bc8b8d7f68a"


class TestStorageImage:
    def test_put_image_by_absent_uuid_should_create_image(self, app: Flask) -> None:
        with app.app_context():
            put_image(_some_image_base64_content, _some_image_uuid)  # Create image

            assert is_image_with_specific_id_exist(_some_image_uuid)

            delete_image(_some_image_uuid)  # Teardown

    def test_delete_image_by_absent_uuid_should_throw_exceptions(
        self, app: Flask
    ) -> None:
        with pytest.raises(FileNotExistError):
            with app.app_context():
                delete_image("a-b-c-d-eeeee")

    def test_delete_image_by_exist_uuid_should_delete_image(self, app: Flask) -> None:
        with app.app_context():
            put_image(_some_image_base64_content, _some_image_uuid)  # Create image
            delete_image(_some_image_uuid)  # Delete image

            assert not is_image_with_specific_id_exist(_some_image_uuid)
