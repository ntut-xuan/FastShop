from __future__ import annotations

from typing import TYPE_CHECKING, no_type_check

import pymysql
import json

from app import current_app

if TYPE_CHECKING:
    from flask import Flask


@no_type_check
def test_invalid_data_on_login(app: Flask) -> None:
    with app.app_context():
        test_client = current_app.test_client()
        data = json.dumps(
            {
                "entroy": "orz",
                "alice": "orz",
                "lai-yt": "orz",
                "jackson": "orz",
                "uriah": "garbage",
            }
        )
        resp = test_client.post(
            "/login", data=data, headers={"content-type": "application/json"}
        )
        assert resp.status_code == 400


@no_type_check
def test_invalid_email_on_login(app: Flask) -> None:
    with app.app_context():
        test_client = current_app.test_client()
        data = json.dumps({"e-mail": "t109590031@ntut@org@tw", "password": "12345678"})
        resp = test_client.post(
            "/login", data=data, headers={"content-type": "application/json"}
        )
        assert resp.status_code == 422
