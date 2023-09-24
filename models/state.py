#!/usr/bin/python3
""" State Module"""

import models
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ Define State class which inherits form BaseModel class

    Attributes:
        name (str): state name
    """
    if models.storage_type == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")
    else:
        @property
        def cities(self):
            """get a list of all related city instances
            with state_id = to the current state id
            """
            FLcity = models.storage.all(models.classes['City']).values()
            return [city for city in FLcity if city.state_id == self.id]
