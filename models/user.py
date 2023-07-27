#!/usr/bin/python3
""" User Module"""

from models import storage_type
from sqlalchemy import Column, String
from models.base_model import BaseModel


class User(BaseModel):
    """ Defines User class that inherits from BaseModel

    Attributes:
        email (str): user email
        password (str): user password
        first_name (str): user first name
        last_name (str): user last name
    """
    __tablename__ = 'users'
    if storage_type == 'db':
        mail = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    email = ""
    password = ""
    first_name = ""
    last_name = ""
