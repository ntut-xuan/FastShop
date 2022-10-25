from datetime import datetime
from json import dumps
from typing import cast

from flask import Blueprint, request
from flask.wrappers import Response

from auth.util import (
    UserProfile,
    login,
    register,
    is_valid_birthday_format,
    is_valid_email,
)
from route.util import Status, fetch_page

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        data = request.json

        if data is None or "e-mail" not in data or "password" not in data:
            return Response(
                dumps(Status.INVALID_DATA.value),
                mimetype="application/json",
                status=400,
            )

        email = data["e-mail"]
        password = data["password"]

        if not is_valid_email(email):
            return Response(
                dumps(Status.INVALID_EMAIL.value),
                mimetype="application/json",
                status=422,
            )

        if not login(email, password):
            return Response(
                dumps(Status.INCORRECT_LOGIN.value),
                mimetype="application/json",
                status=403,
            )

        return Response(dumps(Status.OK.value), mimetype="application/json", status=200)

    return fetch_page("login")


@auth_bp.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        # 400 Bad Request error will automatically be raised
        # if the content-type is not "application/json", so
        # it's safe to cast it manually for type warning supression.
        data = cast(dict, request.json)

        required_columns: list[str] = [
            "firstname",
            "lastname",
            "sex",
            "birthday",
            "e-mail",
            "password",
        ]
        # Check column is exist in json data
        if not all([col in data for col in required_columns]):
            return Response(
                dumps(Status.INVALID_DATA.value),
                mimetype="application/json",
                status=400,
            )

        # Validate the data
        if not is_valid_birthday_format(data["birthday"]):
            return Response(
                dumps(Status.INVALID_DATA.value),
                mimetype="application/json",
                status=422,
            )

        if not is_valid_email(data["e-mail"]):
            return Response(
                dumps(Status.INVALID_EMAIL.value),
                mimetype="application/json",
                status=422,
            )

        profile = UserProfile(
            firstname=data["firstname"],
            lastname=data["lastname"],
            sex=data["sex"],
            birthday=int(datetime.strptime(data["birthday"], "%Y-%m-%d").timestamp()),
        )

        # Register data
        if not register(data["e-mail"], data["password"], profile):
            return Response(
                dumps(Status.INCORRECT_LOGIN.value),
                mimetype="application/json",
                status=403,
            )

        return Response(dumps(Status.OK.value), mimetype="application/json", status=200)

    return fetch_page("register")
