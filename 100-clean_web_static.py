#!/usr/bin/env python3
"""
Fabric script to delete out-of-date archives
"""
from fabric.api import env, run, local, lcd
from datetime import datetime
import os

# Environment variables
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """
    Deletes out-of-date archives from versions and releases folders
    """
    try:
        number = int(number)
        if number < 0:
            return False
    except ValueError:
        return False

    # Fetch all archives in versions folder
    local("ls -1tr versions > archives_versions.txt")
    with open("archives_versions.txt", "r") as file:
        archives_versions = file.readlines()
    archives_versions = [archive.strip() for archive in archives_versions]
    os.remove("archives_versions.txt")

    # Fetch all archives in releases folder
    releases_folder = "/data/web_static/releases/"
    releases_list = run("ls -1tr {} | grep web_static".format(releases_folder))
    archives_releases = releases_list.split()

    # Determine the number of archives to delete
    num_to_delete = len(archives_versions) + len(archives_releases) - number
    if num_to_delete <= 0:
        return True

    # Delete excess archives in versions folder
    for i in range(num_to_delete):
        local("rm -f versions/{}".format(archives_versions[i]))

    # Delete excess archives in releases folder
    for i in range(num_to_delete):
        run("rm -f {}/{}".format(releases_folder, archives_releases[i]))

    return True
