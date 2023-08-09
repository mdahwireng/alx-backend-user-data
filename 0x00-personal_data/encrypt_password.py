#!/usr/bin/env python3
"""Contains password hashing algorithm"""
import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """Hashes a password
    Args:
        password (str): password to be hashed
    """
    if type(password) is not str:
        return b""
    pw: bytes = password.encode('utf-8')
    hashed_pw: bytes = bcrypt.hashpw(pw, bcrypt.gensalt())

    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates @hashed_password with the provided @password"""
    if type(hashed_password) is not bytes or type(password) is not str:
        return False
    dec_pw: bytes = password.encode()

    return bcrypt.checkpw(dec_pw, hashed_password)
