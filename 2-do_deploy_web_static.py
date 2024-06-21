#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers."""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']

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
