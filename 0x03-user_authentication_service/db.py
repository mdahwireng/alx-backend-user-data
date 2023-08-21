#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates a 'User' instance and stores it in the database
        Args:
            email (str): User email
            hashed_password (str): user hashed password
        Returns:
            The created 'User' instance
        """
        u = User(email=email, hashed_password=hashed_password)
        self._session.add(u)
        self._session.commit()

        return u

    def find_user_by(self, **kwargs) -> User:
        """Returns the first row found in the 'Users' table as filtered by
        the method's input arguments
        """
        try:
            res = self._session.query(User).filter_by(**kwargs).first()
            if not res:
                raise NoResultFound

            return res
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Locates and updates a user with @kwargs passed
        Args:
            user_id (int): User ID
            kwargs (dict): column-value to update user Columns with
        Returns:
            None
        """
        for k in kwargs.keys():
            if k not in User.__dict__:
                raise ValueError
        usr = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            setattr(usr, k, v)

        self._session.commit()
