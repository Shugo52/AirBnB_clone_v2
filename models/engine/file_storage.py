#!/usr/bin/python3
""" FileStorage class Module"""

import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.review import Review


class FileStorage:
    """ Defines a 'FileStorage' class

    Attributes:
        file_path: path to JSON file
        object: dictionary
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Defines 'all' method of class

        Returns:
            Dictionary of all cls instances
        """
        # if class name is not given
        if cls is None:
            return FileStorage.__objects

        # Save class name in a variable
        class_name = cls.__name__

        # Create empty dictionary to be returned
        tmp_dict = {}

        # Loop through all keys in __objects
        for key in self.__objects.keys():

            # Check if class_name mathces present key
            if key.split('.')[0] == class_name:

                # Update dictionary
                tmp_dict[key] = self.__objects[key]
        return tmp_dict

    def new(self, obj):
        """ Defines 'new' method
        sets in __objects the obj with key <obj class name>.id
        """
        obj_name = obj.__class__.__name__
        FileStorage.__objects[f"{obj_name}.{obj.id}"] = obj

    def save(self):
        """ Define 'save' method
        serializes __objects to the JSON file
        """
        objs = FileStorage.__objects
        obj_dict = {obj: objs[obj].to_dict() for obj in objs.keys()}
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(obj_dict, f, indent=2)

    def reload(self):
        """ Defines 'reload' method
        deserializes the JSON file if available
        """
        try:
            with open(FileStorage.__file_path) as f:
                objs = json.load(f)
                for obj in objs.values():
                    class_name = obj['__class__']
                    self.new(eval(class_name)(**obj))
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        """Defines delete method to delete and object saved in file"""
        if obj is None:
            return
        obj_key = obj.to_dict()['__class__'] + '.' + obj.id
        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]
        self.save()

    def close(self):
        """"""
        self.reload()
