#!/usr/bin/python3
"""Defines the Amenity class."""

from models import storage_type
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """
    if storage_type == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
