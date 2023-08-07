#!/usr/bin/env python3
"""_summary_"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User


class BasicAuth(Auth):
    """_summary_

    Args:
        Auth (_type_): _description_
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """_summary_

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """_summary_

        Args:
            base64_authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            bstr = b64decode(base64_authorization_header, validate=True)
        except Exception:
            return None
        else:
            return bstr.decode("utf-8")

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """_summary_

        Args:
            self (_type_): _description_
            str (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None

        credentials = decoded_base64_authorization_header.split(":")
        return credentials[0], credentials[1]

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """_summary_

        Args:
            self (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        user = User.search(attributes={"email": user_email})

        if not user:
            return None

        if not user.is_valid_password(user_pwd):
            return None

        return user
