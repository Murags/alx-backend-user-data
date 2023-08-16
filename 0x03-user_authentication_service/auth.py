#!/usr/bin/env python3
"""Auth module"""
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


def _generate_uuid(self) -> str:
    """Generates a uuid"""
    return str(uuid4())
