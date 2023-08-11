#!/usr/bin/python3
"""DBStorage Module"""

from os import getenv
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    """ Defines DBStorage class

    Attributes:
        engine: database engine
        session: database session
    """
    __engine = None
    __session = None

    def __init__(self):
        # Set environment variables
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        enviroment = getenv('HBNB_ENV')

        # initiate connection to mysql
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      user,
                                      password,
                                      host,
                                      database),
                                      pool_pre_ping=True)

        if enviroment == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Defines all method that returns all objects

        Args:
            cls: class of objects to retrieve
        """
        objs = {}
        if cls:
            objs = {obj.__class__.__name__ + "." + obj.id: obj for
                    obj in self.__session.query(classes[cls]).all()}
        else:
            for tbl in Base.__subclasses__():
                table = self.__session.query(tbl).all()
                for obj in table:
                    objs[obj.__class__.__name__ + "." + obj.id] = obj
        return objs

    def new(self, obj):
        """Defines add method that adds obj to the current db session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as ex:
                self.__session.rollback()
                raise ex

    def save(self):
        """Defines save method that commits all changes in current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Defines delete method that deletes an object in current session"""
        if obj:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        """Defines reload method to create db session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)()

    def close(self):
        """Calls close() method of a session"""
        self.__session.close()
