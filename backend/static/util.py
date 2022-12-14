import re
from base64 import b64decode
from pathlib import Path

from flask import current_app

from static.exception import ImageNotExistError


def has_image_with_specific_uuid(image_uuid: str) -> bool:
    """Checks the image with specific `image_uuid` is exist or not.

    Returns:
        bool: The image with specific `image_uuid` is exist or not.
    """
    image_path: Path = get_file_path_by_image_uuid(image_uuid)
    return image_path.exists()


def delete_image(image_uuid: str) -> None:
    """Deletes the image with specific `image_uuid`

    Raises:
        ImageNotExistError: Specific `image_uuid` is not exist.
    """
    image_path: Path = get_file_path_by_image_uuid(image_uuid)
    try:
        image_path.unlink()
    except FileNotFoundError:
        raise ImageNotExistError(image_path)


def write_image_with_byte_data(byte_data: bytes, image_uuid: str) -> None:
    """Writes the byte data to the image file with specific `image_uuid`'"""
    image_path: Path = get_file_path_by_image_uuid(image_uuid)
    image_path.write_bytes(byte_data)


def get_image_byte_from_existing_file(image_uuid: str) -> bytes:
    """Returns the byte data of the image with specific UUID.

    Returns:
        bytes: The bytes data of image.
    """
    image_path: Path = get_file_path_by_image_uuid(image_uuid)
    return image_path.read_bytes()


def get_file_path_by_image_uuid(uuid: str) -> Path:
    """
    Image with its id as `image_id` has path `STATIC_RESOURCE_PATH`/`image_id`.png,
    where `STATIC_RESOURCE_PATH` is configured in config.py.

    Returns:
        Path: The path object contains the path of image file.
    """
    static_resource_path: str = current_app.config.get("STATIC_RESOURCE_PATH")  # type: ignore
    path = Path(f"{static_resource_path}/{uuid}.png")
    return path


def get_image_byte_data_from_base64_content(base64_content: str) -> bytes:
    """Get the byte data of image from base64 content.

    Args:
        base64_content (str): The content formatted `data:image/png;base64,<some base64 data>`.

    Returns:
        bytes: The byte data extract from base64 content
    """
    header, base64_data = base64_content.split(",")
    return b64decode(base64_data)


def verify_image_base64_content(content: str) -> bool:
    """Verify the data of the image using Regex.

    Args:
        content (str): The content formatted `data:image/png;base64,<some base64 data>`.

    Returns:
        bool: The content is valid or not.
    """
    return (
        re.fullmatch("^data:image\/png;base64,[A-Za-z0-9+/]+={0,2}$", content)
        is not None
    )


def verify_uuid(uuid: str) -> bool:
    """Verify the UUID using Regex.

    Returns:
        bool: The UUID is valid or not.
    """
    return (
        re.fullmatch(
            r"^[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}$",
            uuid,
        )
        is not None
    )
