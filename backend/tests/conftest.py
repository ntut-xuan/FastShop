from __future__ import annotations

from typing import TYPE_CHECKING

import pymysql
import pytest

from app import create_app

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(pymysql, "connect", FakeConnection.connect)

    app = create_app({"TESTING": True})

    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


class FakeConnection:
    @staticmethod
    def connect(*args, **kwargs) -> FakeConnection:
        return FakeConnection()

    def __init__(self) -> None:
        self._is_closed = False

    def close(self) -> None:
        self._is_closed = True

    def is_closed(self) -> bool:
        return self._is_closed
