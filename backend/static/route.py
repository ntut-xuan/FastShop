from __future__ import annotations

from flasgger import swag_from
from flask import Blueprint

static_bp = Blueprint("static", __name__)


@static_bp.route("/static/images/<string:id>", methods=["GET"])
@swag_from("../api/static/static_images_id_get.yml")
def fetch_image_with_specific_id(id):
    pass  # pragma: no cover


@static_bp.route("/static/images", methods=["POST"])
@swag_from("../api/static/static_images_post.yml")
def upload_image():
    pass  # pragma: no cover


@static_bp.route("/static/images/<string:id>", methods=["PUT"])
@swag_from("../api/static/static_images_id_put.yml")
def modify_image_with_specific_id(id):
    pass  # pragma: no cover


@static_bp.route("/static/images/<string:id>", methods=["DELETE"])
@swag_from("../api/static/static_images_id_delete.yml")
def delete_image_with_specific_id(id):
    pass  # pragma: no cover
