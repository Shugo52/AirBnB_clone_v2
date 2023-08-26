#!/usr/bin/python3
"""Defines the Amenity class."""

from place import place_amenity
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """
    __tablename__ = 'amenities'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place', secondary=place_amenity,
                                 viewonly=False, back_populates='place_amenities')
    else:
        name = ""
