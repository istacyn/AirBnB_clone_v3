#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

        # Hash the password if it exists in the arguments
        if "password" in kwargs:
            self.password = hashlib.md5(kwargs["password"].encode()).hexdigest()

    def to_dict(self, **kwargs):
        """Returns a dictionary representation of the User instance"""
        # Create a shallow copy of the instance's dictionary
        user_dict = super().to_dict(**kwargs)

        # If the storage type is not 'file', remove the 'password' key from the dictionary
        if models.storage_t != 'file':
            user_dict.pop('password', None)

        return user_dict
