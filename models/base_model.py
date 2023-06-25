#!/usr/bin/python3
""" Base Model Module"""

import cmd
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """ Defines BaseModel class

    Args:
        id (str): uuid generated unique id
        created_at: current datetime instance was created
        updated_at: current datetime instance was updated

    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DATETIME, nullable=False, default=datetime.utcnow())
    updated_at = Column(DATETIME, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    self.__dict__[k] = self.__dict__[k].fromisoformat(v)
                else:
                    self.__dict__[k] = v
        self.save()

    def save(self):
        self.updated_at = datetime.today()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        instanceDict = self.__dict__.copy()
        instanceDict['__class__'] = self.__class__.__name__
        instanceDict['created_at'] = self.created_at.isoformat()
        instanceDict['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in instanceDict.keys():
            del instanceDict["_sa_instance_state"]
        return instanceDict

    def delete(self):
        """Defines delete method to delete current instance in storage"""
        models.storage.delete(self)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
