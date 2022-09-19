from __future__ import annotations
from typing import TYPE_CHECKING

import pytest

from app import create_app

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
