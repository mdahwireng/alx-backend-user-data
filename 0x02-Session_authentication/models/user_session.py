#!/usr/bin/env python3
"""Sessions in Database"""
from models.base import Base
import uuid


class UserSession(Base):
    """Class for storing User Session in Database"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialises a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id", str(uuid.uuid4()))
        self.session_id = kwargs.get("session_id", str(uuid.uuid4()))
