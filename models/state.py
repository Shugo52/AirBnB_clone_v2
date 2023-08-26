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
    __tablename__ = 'states'
    if models.storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            '''returns the list of City instances with state_id
                equals the current State.id
                FileStorage relationship between State and City
            '''
            Rcities = models.storage.all(models.classes['City']).values()
            return [city for city in Rcities if city.state_id == self.id]
