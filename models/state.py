#!/usr/bin/python3
""" State Module"""

import models
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ Define State class which inherits form BaseModel class

    Attributes:
        name (str): state name
    """
    __tablename__ = "states"
    if models.storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")
    else:
        @property
        def cities(self):
            """get a list of all related city instances
            with state_id = to the current state id
            """
            cities_list = []

            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
