from __future__ import annotations

from http import HTTPStatus
from uuid import uuid4

from flasgger import swag_from
from flask import Blueprint, make_response, request

from auth.util import verify_login_or_return_401
from static.util import (
    get_image_byte_data_from_base64_content,
    verify_image_data,
    write_image_with_byte_data,
)
from util import SingleMessageStatus
from response_message import WRONG_DATA_FORMAT

static_bp = Blueprint("static", __name__)


@static_bp.route("/static/images/<string:uuid>", methods=["GET"])
@swag_from("../api/static/static_images_id_get.yml")
def fetch_image_with_specific_id(uuid):
    pass  # pragma: no cover


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
def modify_image_with_specific_id(uuid):
    pass  # pragma: no cover


@static_bp.route("/static/images/<string:uuid>", methods=["DELETE"])
@swag_from("../api/static/static_images_id_delete.yml")
def delete_image_with_specific_id(uuid):
    pass  # pragma: no cover
