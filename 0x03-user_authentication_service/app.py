#!/usr/bin/env python3
"""sample Flask application"""

from flask import Flask, jsonify, request, make_response, abort, redirect
from flask import url_for
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
    user = AUTH.get_user_from_session_id(sesh_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("home"))
    abort(403)


@app.route("/profile", strict_slashes=False)
def profile():
    """Gets the user email based on session"""

    sesh_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sesh_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """gets the reset password token"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
