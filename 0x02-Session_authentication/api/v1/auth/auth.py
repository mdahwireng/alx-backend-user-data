#!/usr/bin/env python3
""" Module for Authenticaton
"""
from flask import request
from typing import (List, TypeVar)


class Auth:
    """Authentication class"""

    def __init__(self):
        """Initialises an 'Auth' instance"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if @path needs authentication before allowing accessing
        """
        if (path is None or
                excluded_paths is None or
                type(excluded_paths) is list and len(excluded_paths) == 0):
            return True
        slash_ends_path = path[-1] == '/'
        if not slash_ends_path:
            path += '/'
        for i in excluded_paths:
            if i[-1] == '*':
                if path.startswith(i[:-1]):
                    return False
            if i == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns None
        """
        if request is None:
            return None

        authorization_key = request.headers.get('Authorization', None)

        return authorization_key

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        import os
        COOKIE_NAME = os.getenv("SESSION_NAME")

        return request.cookies.get(COOKIE_NAME)
