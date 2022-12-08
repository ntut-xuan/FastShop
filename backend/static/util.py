from os import remove
from os.path import exists

from flask import current_app

from static.exception import FileNotExistError


def has_image_with_specific_id (image_id: str) -> bool:
    image_path: str = _get_file_path_by_image_id(image_id)
    return exists(image_path)


def delete_image(image_id: str) -> None:
    image_path: str = _get_file_path_by_image_id(image_id)
    if not has_image_with_specific_id (image_id):
        raise FileNotExistError(image_path)
    else:
        remove(image_path)


def write_static_image(image_data: str, image_id: str) -> None:
    image_path: str = _get_file_path_by_image_id(image_id)
    with open(image_path, "w") as f:
        f.write(image_data)


def _get_file_path_by_image_id(image_id: str) -> str:
    path: str = _get_image_storage_path()
    return path + f"/{image_id}.png"


def _get_image_storage_path() -> str:
    path: str = current_app.config.get("STATIC_RESOURCE_PATH") # type: ignore
    return path
