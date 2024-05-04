#!/usr/bin/python3
"""
This scripty unalives outdated archives
"""

from fabric.api import env

env.hosts = ['54.242.98.93', '35.168.3.68']


def do_clean(number=0):
    """
    Deletes all useless archives in /version &
    in /data/web_static/releases
    """
    from fabric.api import local, run, env

    number = int(number)
    if number == 0:
        number = 1

    # remove local archives
    if env.host_string == env.hosts[0]:  # execute once
        archives = local("ls -tr versions/ | tr ' ' '\\n' |\
                          head -n -{}".format(number), capture=True)
        if archives != '':
            for archive in archives.split('\n'):
                ret = local("rm versions/{}".format(archive))
                if ret.failed:
                    return False

    # remove remote archives
    archives = run("ls -tr --hide=test /data/web_static/releases/ \
                    | tr ' ' '\\n' | head -n -{}".format(number))
    if archives != '':
        for archive in archives.split('\n'):
            ret = run("rm -rf /data/web_static/releases/\
                       {}".format(archive.strip('\r')))
            if ret.failed:
                return False

    return True
