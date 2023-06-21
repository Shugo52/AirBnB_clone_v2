#!/usr/bin/python3
""" Review Module"""

from models.base_model import BaseModel


class Review(BaseModel):
    """ Defines Review class and inherits from BaseModel

    Attributes
        place_id (str): Place.id
        user_id (str): User.id
        text (str): text
    """
    place_id = ""
    user_id = ""
    text = ""
