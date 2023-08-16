#!/usr/bin/env python3
"""
test module for the app
"""
from requests import get, post, put, delete


def register_user(email: str, password: str) -> None:
    """ Tests User registraton
    """
    request = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    response = request.json()
    assert response == {"email": email, "message": "user created"}
    assert request.status_code == 200

    request = post("http://0.0.0.0:5000/users",
                   data={'email': email, "password": password})
    response = request.json()
    assert response == {"message": "email already registered"}
    assert request.status_code == 400


def log_in(email: str, password: str) -> str:
    """ Tests login
    """
    request = post("http://0.0.0.0:5000/sessions",
                   data={'email': email, "password": password})
    response = request.json()
    session_id = request.cookies.get("session_id")
    assert request.status_code == 200
    assert response == {"email": email, "message": "logged in"}
    assert session_id is not None
    return session_id


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests wrong password
    """
    request = post("http://0.0.0.0:5000/sessions",
                   data={'email': email, "password": password})
    assert request.status_code == 401
    assert request.cookies.get("session_id") is None


def profile_logged(session_id: str) -> None:
    """ User profile test logged in
    """
    request = get("http://0.0.0.0:5000/profile",
                  cookies={"session_id": session_id})
    response = request.json()
    assert request.status_code == 200
    assert response == {"email": EMAIL}


def profile_unlogged() -> None:
    """ User profile tests logged out
    """
    request = get("http://0.0.0.0:5000/profile")
    assert request.status_code == 403


def log_out(session_id: str) -> None:
    """ Loggging out test
    """
    request = delete("http://0.0.0.0:5000/sessions",
                     cookies={"session_id": session_id},
                     allow_redirects=True)
    response = request.json()
    history = request.history
    assert request.status_code == 200
    assert len(history) == 1
    assert history[0].status_code == 302
    assert response == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ reset password token test
    """
    request = post("http://0.0.0.0:5000/reset_password",
                   data={"email": email})
    response = request.json()
    reset_token = response.get("reset_token")
    assert request.status_code == 200
    assert isinstance(reset_token, str) is True
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Tests password update
    """
    request = put("http://0.0.0.0:5000/reset_password",
                  data={"email": email, "new_password":
                        new_password, "reset_token":
                        reset_token})
    response = request.json()
    assert request.status_code == 200
    assert response == {"email": email, "message": "Password updated"}


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
