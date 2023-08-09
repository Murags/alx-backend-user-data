#!/usr/bin/env python3
"""_summary_"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import Dict


class SessionAuth(Auth):
    """_summary_

    Args:
        Auth (_type_): _description_
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """_summary_

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if user_id is None or isinstance(user_id, str):
            return None

        sesh_id = str(uuid4())
        SessionAuth.user_id_by_session_id[sesh_id] = user_id

        return sesh_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """_summary_

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None or isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)