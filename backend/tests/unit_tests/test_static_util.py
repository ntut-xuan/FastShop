from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generator

import pytest

from static.exception import ImageNotExistError
from static.util import (
    delete_image,
    has_image_with_specific_id,
    write_image,
)

if TYPE_CHECKING:
    from flask import Flask


@dataclass
class SomeImage:
    uuid: str
    base64_content: str


class TestImageManipulation:
    @pytest.fixture
    def app(self, app: Flask) -> Generator[Flask, None, None]:
        """Shadows the one in conftest.py."""
        static_path: str = tempfile.mkdtemp()
        app.config["STATIC_RESOURCE_PATH"] = static_path

        yield app

        shutil.rmtree(static_path)

    @pytest.fixture
    def some_image(self) -> SomeImage:
        return SomeImage(
            uuid="c11d5bcf-f529-4318-904d-4bc8b8d7f68a",
            base64_content="data:image/png;base64,somecontent",
        )

    def test_write_static_image_with_absent_uuid_should_create_image(
        self, app: Flask, some_image: SomeImage
    ) -> None:
        with app.app_context():
            new_image: SomeImage = some_image

            write_image(new_image.base64_content, new_image.uuid)

            assert has_image_with_specific_id(new_image.uuid)

    def test_delete_image_by_absent_uuid_should_throw_exception(
        self, app: Flask
    ) -> None:
        with app.app_context(), pytest.raises(ImageNotExistError):
            delete_image("an-absent-uuid")

    def test_delete_image_by_exist_uuid_should_delete_image(
        self, app: Flask, some_image: SomeImage
    ) -> None:
        with app.app_context():
            write_image(some_image.base64_content, some_image.uuid)

            delete_image(some_image.uuid)

            assert not has_image_with_specific_id(some_image.uuid)
