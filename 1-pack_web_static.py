#!/usr/bin/python3
"""Fabric script to create .tgz archive for web_static"""

import os.path
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Defines do_pack funtion which
    generates a .tgz file for web_static
    """
    # packs file

    try:
        file = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S")
        local('mkdir -p versions')
        local("tar -cvzf versions/{}.tgz {}".format(
            file, "web_static/"))
        size = os.path.getsize("./versions/{}.tgz".format(file))
        print("web_static packed: versions/{}.tgz -> {}Bytes".format(
            file, size))
    except:
        return None
