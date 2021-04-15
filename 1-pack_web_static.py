#!/usr/bin/python3
""" Create archive for web_static content """


from fabric.api import local
from datetime import datetime
from pathlib import Path


time = datetime.now()
year = time.strftime("%Y")
filename = "web_static_{}{}{}{}{}{}".format(year, time.month, time.day,
                                            time.hour, time.minute,
                                            time.second)


def do_pack():
    """ generate a .tgz archive from the contents of the webstatic folder """
    local("mkdir -p versions")
    local("tar -cvzf versions/{}.tgz web_static".format(filename))
    my_tgz = Path("versions/{}.tgz".format(filename))
    if my_tgz.is_file():
        return "versions/{}.tgz".format(filename)
    else:
        return None
