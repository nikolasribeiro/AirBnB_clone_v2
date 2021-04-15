#!/usr/bin/python3
""" Distribute archive to servers """


from fabric.api import local, env
from fabric.operations import run, put
from datetime import datetime
from pathlib import Path
import os.path


time = datetime.now()
year = time.strftime("%Y")
filename = "web_static_{}{}{}{}{}{}".format(year, time.month, time.day,
                                            time.hour, time.minute,
                                            time.second)
env.hosts = ['ubuntu@34.74.56.196', 'ubuntu@34.73.144.167']
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """ generate a .tgz archive from the contents of the webstatic folder """
    local("mkdir -p versions")
    local("tar -cvzf versions/{}.tgz web_static".format(filename))
    my_tgz = Path("versions/{}.tgz".format(filename))
    if my_tgz.is_file():
        return "versions/{}.tgz".format(filename)
    else:
        return None


def do_deploy(archive_path):
    """ deploy archive to server """
    if not os.path.isfile(archive_path):
        return False
    new_filename = archive_path.split('/')[1]
    folder = ("/data/web_static/releases/" + new_filename.split(".")[0])
    try:
        # puts archive on server
        put(archive_path, '/tmp/')

        # makes director
        run("sudo mkdir -p {}".format(folder))

        # uncompress archive to folder
        run("sudo tar -xzf /tmp/{} -C {}".format(new_filename, folder))

        # delete archive from web server
        run("sudo rm /tmp/{}".format(new_filename))

        # move uncompressed files to proper location
        run("sudo mv {}/web_static/* {}/".format(folder, folder))

        # delete symbolic link /data/web_static/current from the web server
        run("sudo rm -rf {}/web_static".format(folder))
        run("sudo rm -rf /data/web_static/current")

        # create new symbolic link
        run("sudo ln -s {} /data/web_static/current".format(folder))
        print("New version deployed!")
        return True
    except Exception:
        return False
