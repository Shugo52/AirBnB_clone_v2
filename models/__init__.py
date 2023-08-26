#!/usr/bin/python3
"""__init__ magic method for models directory"""
from os import getenv

classes = ["User", "State", "City", "Amenity", "Place", "Review"]

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
