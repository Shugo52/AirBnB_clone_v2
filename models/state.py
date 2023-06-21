#!/usr/bin/python3
""" State Module"""

from models.base_model import BaseModel


class State(BaseModel):
    """ Define State class which inherits form BaseModel class

    Attributes:
        name (str): state name
    """
    name = ""
