import os
import re
from base64 import b64decode

from flask import current_app

from static.exception import ImageNotExistError


def has_image_with_specific_id(image_id: str) -> bool:
    image_path: str = get_file_path_by_image_id(image_id)
    return os.path.exists(image_path)


def delete_image(image_id: str) -> None:
    image_path: str = get_file_path_by_image_id(image_id)
    try:
        os.remove(image_path)
    except FileNotFoundError:
        raise ImageNotExistError(image_path)


def write_image_with_byte_data(image_byte_data: bytes, image_id: str) -> None:
    image_path: str = get_file_path_by_image_id(image_id)
    with open(image_path, "wb") as f:
        f.write(image_byte_data)


def get_image_byte_from_existing_file(image_id: str) -> bytes:
    image_path: str = get_file_path_by_image_id(image_id)
    image_byte_data: bytes
    with open(image_path, "rb") as f:
        image_byte_data = f.read()
    return image_byte_data


def get_file_path_by_image_id(image_id: str) -> str:
    """
    Image with its id as `image_id` has path `STATIC_RESOURCE_PATH`/`image_id`.png,
    where `STATIC_RESOURCE_PATH` is configured in config.py.
    """
    static_resource_path: str = current_app.config.get("STATIC_RESOURCE_PATH")  # type: ignore
    return f"{static_resource_path}/{image_id}.png"


def get_image_byte_data_from_base64_content(image_base64_content: str):
    return b64decode(image_base64_content.split(",")[1].rstrip())


def verify_image_data(image_data: str) -> bool:
    return (
        re.fullmatch("^data:image\/png;base64,[A-Za-z0-9+/]+={0,2}$", image_data)
        is not None
    )
