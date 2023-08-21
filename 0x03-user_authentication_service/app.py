#!/usr/bin/env python3
"""Basic Flask app"""
from flask import abort, Flask, jsonify, redirect, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def get_root():
    """Returns a simple json message"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Endpoint to register a new user"""
    email = request.form.get("email")
    pwd = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, pwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": new_user.email,
                    "message": "user created"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Log in function"""
    email = request.form.get("email")
    pwd = request.form.get("password")
    is_valid_cred = AUTH.valid_login(email, pwd)
    if is_valid_cred is False:
        abort(401)
    else:
        sess_id = AUTH.create_session(email)
    resp = jsonify({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", sess_id)

    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Log out function"""
    from sqlalchemy.orm.exc import NoResultFound

    sess_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", strict_slashes=False)
def profile():
    """Displays user profile"""
    sess_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Return token needed for password reset as JSON"""
    email = request.form.get("email")
    try:
        r_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": r_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Updates a user password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_pwd = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_pwd)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
