from pathlib import Path
from secrets import token_hex
from typing import Any, Mapping

from flask import Flask

from auth.route import auth_bp
from database import connect_database_for_app
from util import fetch_page


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    app = Flask(
        __name__,
        instance_path=str(Path(__file__).parent / "instance"),
        instance_relative_config=True,
        static_folder=(Path(__file__).parents[1] / "static"),
    )
    app.config.from_mapping(
        SECRET_KEY=token_hex(),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.register_blueprint(auth_bp)
    _create_path_if_not_exist(app.instance_path)

    @app.route("/", methods=["GET"])
    def index() -> str:
        return fetch_page("index")

    connect_database_for_app(app)

    return app


def _create_path_if_not_exist(path: str) -> None:
    Path(path).mkdir(exist_ok=True)
