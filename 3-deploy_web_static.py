#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers."""

from fabric.api import local
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_pack():
    """Packs web_static files into .tgz archive."""
    local('mkdir -p versions')
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(now.year,
                                                       now.month,
                                                       now.day,
                                                       now.hour,
                                                       now.minute,
                                                       now.second)
    result = local('tar -cvzf versions/{} web_static'.format(archive_name))
    if result.failed:
        return None
    return 'versions/{}'.format(archive_name)

def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not exists(archive_path):
        return False

    archive_name = archive_path.split('/')[-1]
    folder_name = '/data/web_static/releases/' + archive_name.split('.')[0]

    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(folder_name))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, folder_name))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}/'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(folder_name))
        return True
    except:
        return False

def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
