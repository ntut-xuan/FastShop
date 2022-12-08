import os

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


def write_image(image_data: str, image_id: str) -> None:
    image_path: str = get_file_path_by_image_id(image_id)
    with open(image_path, "w") as f:
        f.write(image_data)


def get_file_path_by_image_id(image_id: str) -> str:
    """
    Image with its id as `image_id` has path `STATIC_RESOURCE_PATH`/`image_id`.png,
    where `STATIC_RESOURCE_PATH` is configured in config.py.
    """
    static_resource_path: str = current_app.config.get("STATIC_RESOURCE_PATH")  # type: ignore
    return f"{static_resource_path}/{image_id}.png"
