#!/usr/bin/python3
"""Fabric script to create .tgz archive for web_static"""

import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Defines do_pack funtion which
    generates a .tgz file for web_static
    """
    # set .tgz file name
    dt = datetime.utcnow()
    file = f"web_static_{dt.year}\
                        {dt.month}\
                        {dt.day}\
                        {dt.hour}\
                        {dt.minute}\
                        {dt.second}.tgz"

    # create versions direction if it does not exist
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    # generate .tgz file
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file
