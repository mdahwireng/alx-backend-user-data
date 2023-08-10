#!/usr/bin/env python3
"""Module for Session Database Authentication"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetiem, timedelta
from models.user_session import UserSession
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """Class for Session Database Authentication"""

    def __init__(self):
        """Initializes a SessionDBAuth instance"""
        super().__init__()

    def create_session(self, user_id=None):
        """Creates and stores new instance of UserSession and returns
        Args:
            user_id (str): User ID
        Returns:
            Session ID
        """
        if user_id is None:
            return None
        u_sess = UserSession(user_id=user_id)
        u_sess.save()
        return u_sess.session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting 'UserSession' in the database
        based on the Session ID from the request cookie
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        u_sess = UserSession.search({"session_id": session_id})
        if u_sess == []:
            return None
        u_sess = u_sess[0].to_json()

        user_id = u_sess.get("user_id")
        if self.session_duration <= 0:
            return user_id
        created_at = u_sess.get("created_at")
        if created_at is None:
            return None
        s_duration_td = timedelta(seconds=self.session_duration)
        if (created_at + s_duration_td) < datetime.now():
            return None

        return user_id

    def destroy_session(self, request=None):
        """Destroys the 'UserSession' based on the Session ID from
        the request cookie
        """
        s_name = getenv("SESSION_NAME")
        s_id = request.cookies.get(s_name)
        u_sess = UserSession.search({"session_id": s_id})
        if u_sess == []:
            return None
        u_sess[0].remove()
