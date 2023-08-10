#!/usr/bin/env python3
"""Module for Session Authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for user with ID, @user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a 'User' ID based on a Session ID @session_id"""
        if session_id is None or type(session_id) is not str:
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        """Returns a 'User' instance based on a cookie value"""
        from models.user import User
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)

        return user

    def destroy_session(self, request=None):
        """Deletes the current logged in user session"""
        if request is None:
            return False
        sess_cookie = self.session_cookie(request)
        if sess_cookie is None:
            return False
        logged_user = self.user_id_for_session_id(sess_cookie)
        if logged_user is None:
            return False
        else:
            try:
                del self.user_id_by_session_id[sess_cookie]
            except Exception as e:
                pass
            finally:
                return True
