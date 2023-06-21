#!/usr/bin/python3
""" Base Model Module"""

import cmd
import uuid
import models
from datetime import datetime


class BaseModel:
    """ Defines BaseModel class

    Args:
        id (str): uuid generated unique id
        created_at: current datetime instance was created
        updated_at: current datetime instance was updated

    Attributes:
        None
    """
    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for k,v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    self.__dict__[k] = self.__dict__[k].fromisoformat(v)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        instanceDict = self.__dict__.copy()
        instanceDict['__class__'] = self.__class__.__name__
        instanceDict['created_at'] = self.created_at.isoformat()
        instanceDict['updated_at'] = self.updated_at.isoformat()
        return instanceDict

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
