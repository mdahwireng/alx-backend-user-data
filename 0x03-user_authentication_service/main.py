#!/usr/bin/env python3
"""End To End Integration Test"""
import requests

API_HOST = '0.0.0.0'
API_PORT = 5000
url = 'http://{}:{}'.format(API_HOST, API_PORT)


def register_user(email: str, password: str) -> None:
    """Tests the '/users' endpoint to create user"""
    endpoint = '/users'
    data = {"email": email, "password": password}
    resp = requests.post(url + endpoint, data)
    expected_response = {"email": email, "message": "user created"}
    assert resp.status_code == 200, "Registration failed"
    assert resp.json() == expected_response, "Wrong output"


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests logging in with wrong password"""
    endpoint = "/sessions"
    data = {"email": email, "password": password}
    resp = requests.post(url + endpoint, data)
    error_msg2 = "'session_id' cookie should not be set"
    assert resp.status_code == 401, "Expected 401 http status code"
    assert resp.cookies.get("session_id") is None, error_msg2


def log_in(email: str, password: str) -> str:
    """Tests logging user in with valid credentials"""
    endpoint = "/sessions"
    data = {"email": email, "password": password}
    resp = requests.post(url + endpoint, data)
    session_id = resp.cookies.get("session_id")
    expected_response = {"email": email, "message": "logged in"}
    error_msg3 = "Log in failed, Invalid Credentials"
    assert resp.status_code == 200, "Log in failed, Invalid Credentials"
    assert session_id is not None, "'session_id' cookie not set"
    assert resp.json() == expected_response, error_msg3

    return session_id


def profile_unlogged() -> None:
    """Testing /profile to check that no user is logged in
    before unauthentication.
    """
    endpoint = "/profile"
    resp = requests.get(url + endpoint)
    error_msg = "Expected 403 status code, but got {} code".format(
            resp.status_code)
    assert resp.status_code == 403, error_msg


def profile_logged(session_id: str) -> None:
    """Test /profile to check that user stays logged in after
    passing authentication
    """
    endpoint = "/profile"
    session = requests.Session()
    cookies = {"session_id": session_id}
    url_e = url + endpoint
    req = requests.Request(method="GET", url=url_e, cookies=cookies)
    prepared_req = req.prepare()
    resp = session.send(prepared_req)

    assert resp.status_code == 200, "User not logged in, session expired"
    assert resp.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Tests /sessions for logging out"""
    endpoint = "/sessions"
    session = requests.Session()
    cookies = {"session_id": session_id}
    url_e = url + endpoint
    req = requests.Request(method="DELETE", url=url_e, cookies=cookies)
    prepared_req = req.prepare()
    resp = session.send(prepared_req)
    error_msg1 = "Invalid user session_id, {}".format(resp.status_code)

    assert resp.status_code == 200, error_msg1
    assert "/sessions" not in resp.url, "Invalid user session_id"


def reset_password_token(email: str) -> str:
    """Tests /reset_password for generaing reset password"""
    endpoint = "/reset_password"
    resp = requests.post(url + endpoint, {"email": email})

    resp_reset_token = resp.json().get("reset_token")
    resp_email = resp.json().get("email")
    error_msg1 = "Unexpected status code received: expected 200 but received "
    error_msg1 += str(resp.status_code)
    error_msg2 = "Reset token not returned in json body"

    assert resp.status_code == 200, error_msg1
    assert resp_email == email, "Returned email in json incorrect"
    assert resp_reset_token is not None, error_msg2

    return resp_reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests /reset_password for updating password"""
    endpoint = "/reset_password"
    resp = requests.put(url + endpoint, {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password})
    try:
        sess_id = log_in(email, new_password)
        if sess_id:
            logged_in = True
            log_out(sess_id)  # Log out affect testing new password
    except AssertionError:
        logged_in = False

    error_msg1 = "Wrong status code returned, expected 200 but got "
    error_msg1 += str(resp.status_code)
    assert resp.status_code == 200, error_msg1
    assert logged_in is True, "New password wasn't updated"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
