#!/usr/bin/python3
""" Review Module"""

from models import storage_type
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Defines Review class and inherits from BaseModel

    Attributes
        place_id (str): Place.id
        user_id (str): User.id
        text (str): text
    """
    __tablename__ = 'reviews'
    if storage_type == 'db':
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
