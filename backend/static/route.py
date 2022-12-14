from __future__ import annotations

from http import HTTPStatus
from uuid import uuid4

from flasgger import swag_from
from flask import Blueprint, make_response, send_file, abort, request

from auth.util import verify_login_or_return_401
from static.util import (
    delete_image,
    get_image_byte_data_from_base64_content,
    get_file_path_by_image_id,
    has_image_with_specific_id,
    verify_image_data,
    write_image_with_byte_data,
)
from util import SingleMessageStatus
from response_message import WRONG_DATA_FORMAT

static_bp = Blueprint("static", __name__)


@static_bp.route("/static/images/<string:uuid>", methods=["GET"])
@swag_from("../api/static/static_images_id_get.yml")
def fetch_image_with_specific_id(uuid):
    if not has_image_with_specific_id(uuid):
        status = SingleMessageStatus(
            HTTPStatus.NOT_FOUND, "The image with a specific UUID is absent."
        )
        return make_response(status.message, status.code)
    return send_file(get_file_path_by_image_id(uuid), mimetype="image/png")


@static_bp.route("/static/images", methods=["POST"])
@swag_from("../api/static/static_images_post.yml")
@verify_login_or_return_401
def upload_image():
    image_base64_content: str = request.data.decode("utf-8")

    if not verify_image_data(image_base64_content):
        status = SingleMessageStatus(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)
        return make_response(status.message, status.code)

    image_byte_data: str = get_image_byte_data_from_base64_content(image_base64_content)
    image_uuid_string: str = str(uuid4())
    write_image_with_byte_data(image_byte_data, image_uuid_string)

    response_payload = {"uuid": image_uuid_string}
    return make_response(response_payload)


@static_bp.route("/static/images/<string:uuid>", methods=["PUT"])
@swag_from("../api/static/static_images_id_put.yml")
@verify_login_or_return_401
def modify_image_with_specific_id(uuid):
    image_base64_content: str = request.data.decode("utf-8")

    if not has_image_with_specific_id(uuid):
        status = SingleMessageStatus(
            HTTPStatus.FORBIDDEN, "The image with a specific UUID is absent."
        )
        return make_response(status.message, status.code)

    if not verify_image_data(image_base64_content):
        status = SingleMessageStatus(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)
        return make_response(status.message, status.code)

    image_byte_data: str = get_image_byte_data_from_base64_content(image_base64_content)
    write_image_with_byte_data(image_byte_data, uuid)

    status = SingleMessageStatus(HTTPStatus.OK)
    return make_response(status.message, status.code)


@static_bp.route("/static/images/<string:uuid>", methods=["DELETE"])
@swag_from("../api/static/static_images_id_delete.yml")
@verify_login_or_return_401
def delete_image_with_specific_id(uuid):
    if not has_image_with_specific_id(uuid):
        status = SingleMessageStatus(
            HTTPStatus.FORBIDDEN, "The image with a specific UUID is absent."
        )
        return make_response(status.message, status.code)

    delete_image(uuid)

    status = SingleMessageStatus(HTTPStatus.OK)
    return make_response(status.message, status.code)
