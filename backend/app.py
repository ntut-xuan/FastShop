from pathlib import Path
from typing import Any, Mapping

from flask import Flask


def create_app(test_config: Mapping[str, Any] = None) -> Flask:
    app = Flask(
        __name__,
        instance_path=str(Path(__file__).parent / "instance"),
        instance_relative_config=True,
    )
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    _create_path_if_not_exist(app.instance_path)

    @app.route("/", methods=["GET"])
    def index():
        return "Hello World"

    return app


def _create_path_if_not_exist(path: str) -> None:
    Path(path).mkdir(exist_ok=True)
