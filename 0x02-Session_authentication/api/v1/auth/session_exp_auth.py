#!/usr/bin/env python3
"""Module for Session cookie expiration"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Contains methods neeed to handle session cookie expiration"""

    def __init__(self):
        """Initializes a 'SessionExpAuth instance"""
        try:
            self.session_duration = int(getenv("SESSION_DURATION"))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session_id for user with id, @user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        SessionExpAuth.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a 'User' ID based on a Session ID @session_id"""
        if session_id is None:
            return None
        session_dict = SessionExpAuth.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        user_id = session_dict.get("user_id")
        if self.session_duration <= 0:
            return user_id
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        s_duration_td = timedelta(seconds=self.session_duration)
        if (created_at + s_duration_td) < datetime.now():
            return None

        return user_id
