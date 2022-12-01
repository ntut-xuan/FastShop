from pathlib import Path
from secrets import token_hex
from typing import Any, Mapping

from flasgger import Swagger
from flask import Flask

from auth.route import auth_bp
from database import create_db_command, db
from util import fetch_page


def init_swagger(app: Flask) -> None:
    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config[
        "swagger_ui_bundle_js"
    ] = "//unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"
    swagger_config[
        "swagger_ui_standalone_preset_js"
    ] = "//unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"
    swagger_config["jquery_js"] = "//unpkg.com/jquery@2.2.4/dist/jquery.min.js"
    swagger_config[
        "swagger_ui_css"
    ] = "//unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css"

    Swagger(app)


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

    init_swagger(app)
    db.init_app(app)
    app.cli.add_command(create_db_command)
    app.register_blueprint(auth_bp)

    @app.route("/", methods=["GET"])
    def index() -> str:
        return fetch_page("index")

    return app
