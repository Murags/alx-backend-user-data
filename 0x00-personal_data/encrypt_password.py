#!/usr/bin/env python3
"""_summary_"""
import bcrypt


def hash_password(password: str) -> bytes:
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


def is_valid(hashed_pwd: bytes, password: str) -> bool:
    """_summary_

    Args:
        hashed_pwd (bytes): _description_
        password (str): _description_

    Returns:
        bool: _description_
    """
    if bcrypt.checkpw(password.encode("utf-8"), hashed_pwd):
        return True
    return False
