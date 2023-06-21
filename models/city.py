#!/usr/bin/python3

from models.base_model import BaseModel


class City(BaseModel):
    """ Defines City which inherits form BaseModel

    Attributes:
        state_id (str): would be State.id
        name (str): city name
    """
    state_id = ""
    name = ""
