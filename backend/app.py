from pathlib import Path
from secrets import token_hex
from typing import Any, Mapping

from flask import Flask, current_app

from database.util import connect_database_for_app


def fetch_page(page_name: str) -> str:
    with current_app.open_resource(f"../html/{page_name}.html", mode="r") as page:
        return page.read()


def create_app(test_config: Mapping[str, Any] = None) -> Flask:
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

    _create_path_if_not_exist(app.instance_path)

    @app.route("/", methods=["GET"])
    def index():
        return fetch_page("index")

    @app.route("/login", methods=["GET"])
    def login():
        return fetch_page("login")

    @app.route("/register", methods=["GET"])
    def register():
        return fetch_page("register")

    @app.route("/items", methods=["GET"])
    def items():
        return fetch_page("item_list")

    connect_database_for_app(app)

    return app


def _create_path_if_not_exist(path: str) -> None:
    Path(path).mkdir(exist_ok=True)
