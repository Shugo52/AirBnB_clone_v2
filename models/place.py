#!/usr/bin/python3
""" Place Module"""

from models.base_model import BaseModel


class Place(BaseModel):
    """ Defines Place class and inherits from BaseModel

    Attributes:
        city_id (str): City.id
        user_id (str): User.id
        name (str): Place name
        description (str): description
        number_rooms (int): number of rooms
        number_bathrooms (int): number of bathrooms
        max_guest (int): maximum number of guest
        price_by_night (int): cost per night
        latitude (float): latitude of place
        longitude (float): longitude of place
        amenity_ids (list): list of Amenity.id
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

