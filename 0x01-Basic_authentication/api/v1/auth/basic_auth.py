#!/usr/bin/env python3
"""_summary_"""
from api.v1.auth.auth import Auth


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
