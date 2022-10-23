from json import dumps

from flask import Blueprint, request
from flask.wrappers import Response

from auth.util import login, validate_email
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


@auth.route("/register", methods=["GET"])
def register_route():
    return fetch_page("register")