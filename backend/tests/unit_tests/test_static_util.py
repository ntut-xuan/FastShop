from __future__ import annotations

from base64 import b64decode
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from static.exception import ImageNotExistError
from static.util import (
    delete_image,
    get_file_path_by_image_uuid,
    get_image_byte,
    get_image_byte_data_from_base64_content,
    has_image_with_specific_uuid,
    verify_image_base64_content,
    verify_uuid,
    write_image_with_byte_data,
)

if TYPE_CHECKING:
    from flask import Flask


@dataclass
class SomeImage:
    uuid: str
    byte_data: bytes


class TestImageManipulation:
    @pytest.fixture
    def some_image(self) -> SomeImage:
        return SomeImage(
            uuid="c11d5bcf-f529-4318-904d-4bc8b8d7f68a",
            byte_data=b"does_not_matter",
        )

    def test_write_static_image_with_absent_uuid_should_create_image(
        self, app: Flask, some_image: SomeImage
    ) -> None:
        with app.app_context():
            new_image: SomeImage = some_image

            write_image_with_byte_data(new_image.byte_data, new_image.uuid)

            assert has_image_with_specific_uuid(new_image.uuid)

    def test_write_static_image_with_existing_uuid_should_update_image(
        self, app: Flask, some_image: SomeImage
    ) -> None:
        with app.app_context():
            write_image_with_byte_data(some_image.byte_data, some_image.uuid)
            new_byte_content: bytes = get_image_byte_data_from_base64_content(
                "data:image/png;base64,bmV3X2NvbnRlbnQ="
            )  # The base64 encoding of new_content

            write_image_with_byte_data(new_byte_content, some_image.uuid)

            file_content = get_file_path_by_image_uuid(some_image.uuid).read_bytes()
            assert file_content == new_byte_content

    def test_delete_image_with_absent_uuid_should_throw_exception(
        self, app: Flask
    ) -> None:
        with app.app_context(), pytest.raises(ImageNotExistError):
            delete_image("an-absent-uuid")

    def test_delete_image_with_existing_uuid_should_delete_image(
        self, app: Flask, some_image: SomeImage
    ) -> None:
        with app.app_context():
            write_image_with_byte_data(some_image.byte_data, some_image.uuid)

            delete_image(some_image.uuid)

            assert not has_image_with_specific_uuid(some_image.uuid)

    def test_get_image_byte_with_base64_content_should_return_correct_byte_data(
        self,
    ) -> None:
        base64_content = "data:image/png;base64,ZG9lc19ub3RfbWF0dGVy"  # The base64 encoding of does_not_matter

        bytes_data = get_image_byte_data_from_base64_content(base64_content)

        assert bytes_data == b64decode("ZG9lc19ub3RfbWF0dGVy")

    def test_get_image_byte_with_exist_file_should_return_correct_byte_data(
        self, app: Flask, some_image: SomeImage
    ) -> None:
        with app.app_context():
            new_image: SomeImage = some_image
            write_image_with_byte_data(new_image.byte_data, new_image.uuid)

            bytes_data = get_image_byte(new_image.uuid)

            assert bytes_data == new_image.byte_data


def test_verify_image_with_invalid_data_should_return_false() -> None:
    assert not verify_image_base64_content(f"data:image/png;base64,_____________==")


@pytest.mark.parametrize(
    argnames=("bad_uuid",),
    argvalues=(
        ("AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE-",),  # Redundant dash in back of string
        ("-AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE",),  # Redundant dash in front of uuid
        ("A-B-C-D-E",),  # Not enough length in every segment
        ("A-B-C",),  # Not enough segment
        (
            "________-____-____-____-____________",
        ),  # Correct length of segment but invalid character.
    ),
)
def test_verify_uuid_with_invalid_data_should_return_false(bad_uuid: str) -> None:
    assert not verify_uuid(bad_uuid)
