from pathlib import Path
from secrets import token_hex
from typing import Any, Mapping

from flask import Flask

from auth.route import auth_bp
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

    db.init_app(app)
    app.cli.add_command(create_db_command)
    app.register_blueprint(auth_bp)

    @app.route("/", methods=["GET"])
    def index() -> str:
        return fetch_page("index")

    return app
