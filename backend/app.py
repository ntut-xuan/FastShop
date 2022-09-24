from pathlib import Path
from secrets import token_hex
from typing import Any, Mapping

from flask import Flask, send_from_directory


def fetch_page(page_name: str) -> str:
    with open(f"/etc/fastshop/html/{page_name}.html") as page:
        return page.read()


def create_app(test_config: Mapping[str, Any] = None) -> Flask:
    app = Flask(
        __name__,
        instance_path=str(Path(__file__).parent / "instance"),
        instance_relative_config=True,
        static_url_path="",
    )
    app.config.from_mapping(
        SECRET_KEY=token_hex(),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    _create_path_if_not_exist(app.instance_path)

    @app.route("/static/<path:path>", methods=["GET"])
    def return_static_file(path):
        return send_from_directory("/etc/fastshop/static", path)

    @app.route("/", methods=["GET"])
    def index():
        return fetch_page("index")

    return app


def _create_path_if_not_exist(path: str) -> None:
    Path(path).mkdir(exist_ok=True)
