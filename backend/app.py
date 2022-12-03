from pathlib import Path
from secrets import token_hex
from typing import Any, Final, Mapping

from flasgger import Swagger
from flask import Flask

from auth.route import auth_bp
from tag.route import tag_bp
from database import create_db_command, db
from util import fetch_page


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(
        __name__,
        static_folder=(Path(__file__).parents[1] / "static"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.from_mapping(test_config)
    # a random key for jwt encoding
    app.config["jwt_key"] = token_hex()

    _init_swagger(app)
    db.init_app(app)
    app.cli.add_command(create_db_command)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tag_bp)

    @app.route("/", methods=["GET"])
    def index() -> str:
        return fetch_page("index")

    return app


def _init_swagger(app: Flask) -> None:
    SWAGGER_UI_VERSION: Final[str] = "4.15.5"
    JQUERY_VERSION: Final[str] = "3.6.1"

    SWAGGER_UI_DIST_URL: Final[
        str
    ] = f"//unpkg.com/swagger-ui-dist@{SWAGGER_UI_VERSION}"

    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config[
        "swagger_ui_bundle_js"
    ] = f"{SWAGGER_UI_DIST_URL}/swagger-ui-bundle.js"
    swagger_config[
        "swagger_ui_standalone_preset_js"
    ] = f"{SWAGGER_UI_DIST_URL}/swagger-ui-standalone-preset.js"
    swagger_config["swagger_ui_css"] = f"{SWAGGER_UI_DIST_URL}/swagger-ui.css"
    swagger_config[
        "jquery_js"
    ] = f"//unpkg.com/jquery@{JQUERY_VERSION}/dist/jquery.min.js"

    Swagger(app)
