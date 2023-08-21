#!/usr/bin/env python3
"""Module for Hashed Password"""
from bcrypt import checkpw, hashpw, gensalt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar, Union
from user import User

U = TypeVar(User)


def _hash_password(password: str) -> bytes:
    """Returns the salted hash of @password, hashed with bcrypt.hashpw
    """
    salt = gensalt()
    h_pw = hashpw(password.encode(), salt)
    return h_pw


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID"""
    from uuid import uuid4
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Creates a 'User' instance and saves it to the database"""
        try:
            user_by_email = self._db.find_user_by(email=email)
            if user_by_email:
                raise ValueError("User {} already exists".format(
                    user_by_email.email))
        except NoResultFound:
            h_pwd = _hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=h_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Queries the database to check if @email and @password passed
        matches existing data
        """
        if type(email) is not str or type(password) is not str:
            return False
        e_pwd = password.encode()
        try:
            user_by_email = self._db.find_user_by(email=email)
            is_valid = checkpw(e_pwd, user_by_email.hashed_password)
            return is_valid
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session ID and stores it in the DB with
        the corresponding user with the email, @email
        """
        try:
            user_by_email = self._db.find_user_by(email=email)
            user_id = user_by_email.id
            s_id = _generate_uuid()
            self._db.update_user(user_id, session_id=s_id)

            return s_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, U]:
        """Returns the 'User' object with the corresponding @session_id"""
        if type(session_id) is not str:
            return None
        try:
            user_by_sess_id = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user_by_sess_id

    def destroy_session(self, user_id: int) -> None:
        """Deletes the 'session_id' value/column of the
        'User' instance with @user_id
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Initiates the password recovery phase by updating the 'reset_token'
        field of an exist 'User' with a unique UUID generated
        """
        try:
            user = self._db.find_user_by(email=email)
            r_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=r_token)
        except NoResultFound:
            raise ValueError

        return r_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the 'hashed_password' field of a 'User' instance"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        h_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=h_pwd, reset_token=None)
