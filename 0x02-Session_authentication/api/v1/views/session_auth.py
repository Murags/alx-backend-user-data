#!/usr/bin/env python3
"""_summary_"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.user import User
from os import getenv


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def login():
    """_summary_

    Returns:
        _type_: _description_
    """
    email = request.form.get("email")
    pwd = request.form.get("password")

    if not email or email is None:
        return jsonify({"error": "email missing"}), 400
    if not pwd or pwd is None:
        return jsonify({"error": "password missing"}), 400

    user_inst = User.search({"email": email})
    if user_inst is None:
        return jsonify({"error": "no user found for this email"}), 404
    curr_user = None
    for user in user_inst:
        if user.is_valid_password(pwd):
            curr_user = user
            break
    if curr_user is None:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    sesh_id = auth.create_session(curr_user.get("id"))
    response = jsonify(curr_user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), sesh_id)

    return response

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """_summary_

    Returns:
        _type_: _description_
    """
    from api.v1.app import auth
    status = auth.destroy_session(request)
    if not status:
        abort(404)
    return jsonify({}), 200
