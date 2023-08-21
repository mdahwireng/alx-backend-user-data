#!/usr/bin/env python3
"""User model"""
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """An SQLAlchemy Database schema named 'users'"""

    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    email = Column("email", VARCHAR(250), nullable=False)
    hashed_password = Column("hashed_password", VARCHAR(250), nullable=False)
    session_id = Column("session_id", VARCHAR(250))
    reset_token = Column("reset_token", VARCHAR(250))
