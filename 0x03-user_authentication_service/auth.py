#!/usr/bin/env python3
"""Auth module"""
from typing import Optional
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""
        hash_pwd = _hash_password(password)

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            user = self._db.add_user(email, hash_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the user login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """Creates a user a session and return the session id"""
        try:
            user = self._db.find_user_by(email=email)
            sesh_id = _generate_uuid()
            user.session_id = sesh_id
            return sesh_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Gets user from database using the session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str):
        """Destroys a session of a User"""
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """generates a password reset token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            user.reset_token = token
            return token
        except Exception:
            raise ValueError


def _hash_password(password):
    """_summary_

    Args:
        password (str): _description_

    Returns:
        bytes: _description_
    """
    encd_pwd = password.encode("utf-8")
    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(encd_pwd, salt)

    return hashed_pwd


def _generate_uuid() -> str:
    """Generates a uuid"""
    return str(uuid4())
