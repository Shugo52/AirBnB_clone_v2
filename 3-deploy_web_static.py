#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.api import local
from datetime import datetime

env.hosts = ["54.234.76.194", "100.26.171.250"]
env.user = 'ubuntu'


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


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False

    try:
        file = archive_path.split("/")[-1]
        name = file.split('.')[0]
        put(archive_path, '/tmp/{}'.format(file))
        run('mkdir -p /data/web_static/releases/{}'.format(name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'
            .format(file, name))
        run('rm /tmp/{}'.format(file))
        run('mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/'.format(name, name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/\
        /data/web_static/current'.format(name))
        print("New version deployed!")
        return True
    except:
        print("New version not deployed...")
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
