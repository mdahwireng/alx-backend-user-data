#!/usr/bin/env python3
"""View for all session authentication related endpoint
"""
from api.v1.views import app_views
from flask import Blueprint, jsonify, request


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def log_in():
    """Route for submitting logging data"""
    from models.user import User
    import os

    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return jsonify({
            "error": "email missing"
            }), 400
    if password is None:
        return jsonify({
            "error": "password missing"
            }), 400
    user_by_email = User.search({"email": email})
    if user_by_email == []:
        return jsonify({
            "error": "no user found for this email"
            }), 404
    user_by_email = user_by_email[0]
    if not user_by_email.is_valid_password(password):
        return jsonify({
            "error": "wrong password"
            }), 401
    else:
        from api.v1.app import auth
        user_id = user_by_email.id
        session_id = auth.create_session(user_id)
        session_name = os.getenv("SESSION_NAME")
        out = jsonify(user_by_email.to_json())
        out.set_cookie(session_name, session_id)
        return out


@app_views.route("/auth_session/logout",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_session():
    """Logs user out by deleting Session ID"""
    from api.v1.app import auth
    destroyed_sess = auth.destroy_session(request)
    if destroyed_sess is False:
        abort(404)

    return jsonify({}), 200
