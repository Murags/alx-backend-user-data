#!/usr/bin/env python3
"""_summary_"""
from api.v1.auth.auth import Auth
from base64 import b64decode


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
