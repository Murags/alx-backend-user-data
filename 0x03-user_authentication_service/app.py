#!/usr/bin/env python3
"""sample Flask application"""

from flask import Flask, jsonify, request, make_response, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home() -> str:
    """Return a a json message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """Adds a user to a database using the AUTH"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Creates a cookie session"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        sesh_id = AUTH.create_session(email)
        res = make_response(jsonify({"email": email, "message": "logged in"}))
        res.set_cookie("session_id", sesh_id)
        return res

    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """destroys a cookie session"""
    sesh_id = request.cookies.get("session_id")
    if sesh_id:
        user = AUTH.get_user_from_session_id(sesh_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
