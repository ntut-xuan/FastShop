from datetime import datetime
from json import dumps
from typing import cast

from flask import Blueprint, request
from flask.wrappers import Response

from auth.util import Profile, login, register, validate_birthday_format, validate_email
from route.util import Status, fetch_page

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login_route():
    def get():
        return fetch_page("login")

    def post():
        data = request.json

        if data is None or "e-mail" not in data or "password" not in data:
            return Response(
                dumps(Status.INVALID_DATA.value),
                mimetype="application/json",
                status=400,
            )

        email = data["e-mail"]
        password = data["password"]

        if not validate_email(email):
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

    if request.method == "GET":
        return get()
    else:  # POST
        return post()


@auth.route("/register", methods=["GET", "POST"])
def register_route():
    def get():
        return fetch_page("register")

    def post():
        # 400 Bad Request error will automatically be raised
        # if the content-type is not "application/json", so
        # it's safe to cast it manually for type warning supression.
        data = cast(dict, request.json)

        require_columns: list[str] = [
            "firstname",
            "lastname",
            "sex",
            "birthday",
            "e-mail",
            "password",
        ]
        # Check column is exist in json data
        if not all([col in data for col in require_columns]):
            return Response(
                dumps(Status.INVALID_DATA.value),
                mimetype="application/json",
                status=400,
            )

        # Build the parameter variable
        email = data["e-mail"]
        password = data["password"]

        # Validate the data
        if not validate_birthday_format(data["birthday"]):
            return Response(
                dumps(Status.INVALID_DATA.value),
                mimetype="application/json",
                status=422,
            )

        if not validate_email(email):
            return Response(
                dumps(Status.INVALID_EMAIL.value),
                mimetype="application/json",
                status=422,
            )

        profile = Profile(
            firstname=data["firstname"],
            lastname=data["lastname"],
            sex=data["sex"],
            birthday=int(datetime.strptime(data["birthday"], "%Y-%m-%d").timestamp()),
        )

        # Register data
        if not register(email, password, profile):
            return Response(
                dumps(Status.INCORRECT_LOGIN.value),
                mimetype="application/json",
                status=403,
            )

        return Response(dumps(Status.OK.value), mimetype="application/json", status=200)

    if request.method == "GET":
        return get()
    else:  # POST
        return post()
