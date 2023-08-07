#!/usr/bin/env python3

from typing import List, TypeVar

class Auth:

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        plus = path+"/"
        if path in excluded_paths:
            return False
        if plus in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        if request is None:
            return None
        if "Authorization" not in request.keys():
            return None

        return request["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        return None
