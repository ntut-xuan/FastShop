from flask import Flask, current_app, Blueprint, request

from route.util import fetch_page
from auth.util import login


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    def get():
        return fetch_page("login")

    def post():
        pass

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


@auth.route("/register", methods=["GET"])
def register():
    return fetch_page("register")
