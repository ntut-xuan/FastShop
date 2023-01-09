from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from uuid import uuid4

from flask import Blueprint, make_response, request, send_file

from src.auth.util import verify_login_or_return_401
from response_message import (
    ABSENT_IMAGE_WITH_SPECIFIC_UUID,
    INVALID_UUID,
    WRONG_DATA_FORMAT,
)
from src.static.util import (
    delete_image,
    get_file_path_by_image_uuid,
    get_image_byte_data_from_base64_content,
    has_image_with_specific_uuid,
    verify_image_base64_content,
    verify_uuid,
    write_image_with_byte_data,
)
from util import make_single_message_response, route_with_doc

if TYPE_CHECKING:
    from flask.wrappers import Response

static_bp = Blueprint("static", __name__)


@route_with_doc(static_bp, "/static/images/<string:uuid>", methods=["GET"])
def fetch_image_with_specific_id(uuid: str) -> Response:
    if not verify_uuid(uuid):
        return make_single_message_response(HTTPStatus.FORBIDDEN, INVALID_UUID)

    if not has_image_with_specific_uuid(uuid):
        return make_single_message_response(
            HTTPStatus.NOT_FOUND, ABSENT_IMAGE_WITH_SPECIFIC_UUID
        )

    return send_file(get_file_path_by_image_uuid(uuid), mimetype="image/png")


@route_with_doc(static_bp, "/static/images", methods=["POST"])
@verify_login_or_return_401
def upload_image() -> Response:
    image_base64_content: str = request.data.decode("utf-8")

    if not verify_image_base64_content(image_base64_content):
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    image_byte_data: bytes = get_image_byte_data_from_base64_content(
        image_base64_content
    )
    image_uuid = str(uuid4())
    write_image_with_byte_data(image_byte_data, image_uuid)

    response_payload: dict[str, str] = {"uuid": image_uuid}
    return make_response(response_payload)


@route_with_doc(static_bp, "/static/images/<string:uuid>", methods=["PUT"])
@verify_login_or_return_401
def modify_image_with_specific_id(uuid: str) -> Response:
    image_base64_content: str = request.data.decode("utf-8")

    if not verify_uuid(uuid):
        return make_single_message_response(HTTPStatus.FORBIDDEN, INVALID_UUID)

    if not has_image_with_specific_uuid(uuid):
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, ABSENT_IMAGE_WITH_SPECIFIC_UUID
        )

    if not verify_image_base64_content(image_base64_content):
        return make_single_message_response(HTTPStatus.BAD_REQUEST, WRONG_DATA_FORMAT)

    image_byte_data: bytes = get_image_byte_data_from_base64_content(
        image_base64_content
    )
    write_image_with_byte_data(image_byte_data, uuid)

    return make_single_message_response(HTTPStatus.OK)


@route_with_doc(static_bp, "/static/images/<string:uuid>", methods=["DELETE"])
@verify_login_or_return_401
def delete_image_with_specific_id(uuid: str) -> Response:
    if not verify_uuid(uuid):
        return make_single_message_response(HTTPStatus.FORBIDDEN, INVALID_UUID)

    if not has_image_with_specific_uuid(uuid):
        return make_single_message_response(
            HTTPStatus.FORBIDDEN, ABSENT_IMAGE_WITH_SPECIFIC_UUID
        )

    delete_image(uuid)

    return make_single_message_response(HTTPStatus.OK)
