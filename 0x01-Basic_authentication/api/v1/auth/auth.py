#!/usr/bin/env python3
"""_summary_"""
from flask import request
from typing import List, TypeVar


class Auth:
    """_summary_
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        plus = path+"/"
        if path in excluded_paths:
            return False
        if plus in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if path.startswith(excluded_path.strip("*")):
                return False
            if plus.startswith(excluded_path.strip("*")):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_

        Returns:
            _type_: _description_
        """
        return None
