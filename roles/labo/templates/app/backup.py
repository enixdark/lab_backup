from __future__ import absolute_import

import sys
import os
import shutil
import ConfigParser
from pathlib import Path
import subprocess
import datetime
import docker
from optparse import OptionParser

from utils.logger import Logger
from utils.constants import Constant

config = ConfigParser.ConfigParser()
logger = Logger(__name__)
use_docker = bool(os.getenv('USE_DOCKER') or False)
client = docker.from_env()
user = os.getenv('USER') or 'root'

def get_config():
    conf = None
    try:
        with open('config.ini') as f:
            conf = config.readfp(f)
    except (OSError, IOError,) as e:
        logger.error(e.message)
    return conf


def call_run(func):
    def wrapper(*args, **kwargs):
        cmd = func(*args, **kwargs)
        logger.info("use command %s for backup" % cmd)
        return client.containers.get(os.getenv('CONTAINER_NAME')).exec_run(cmd) if use_docker else subprocess.call([cmd], shell=True)
    return wrapper

# get list folders and files based on path nd sorted by time
def get_lists(path):
    if os.path.exists(path):
        return [ str(raw_path) for raw_path in sorted(Path(path).iterdir(), key=lambda f: f.stat().st_mtime)]



# use cp command to backup a folder or file from directory to other directory 
@call_run 
def backup_with_cp(from_dir, to_dir, rsync=False):
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    logger.info('create new backup at %s in %s' % (datetime.datetime.now(), to_dir))
    return (Constant.Command.RSYNC % (user, user, from_dir, to_dir)) if rsync else (Constant.Command.CP % (from_dir, to_dir))

# use mongodump command to create a backup
@call_run
def backup_with_mongodump(uri=None, database=None, collection=None, to_dir="dump"):
    logger.info('create new backup at %s in %s' % (datetime.datetime.now(), to_dir))
    return (Constant.Command.MONGODUMP 
          + (' -h %s' % uri if database else '') 
          + (' -d %s' % database if database else '') 
          + (' -c %s' % collection if collection else '') 
          + ' -o %s' % to_dir)

def limited_process(term, **kwargs):
    list_dirs = []
    if isinstance(term, list):
        list_dirs = term
    elif isinstance(term, str):
        if Path(term).exists():
            list_dirs = get_lists(term)
            
    if len(list_dirs) > kwargs.get('limited'):
        for d in list_dirs[0:(len(list_dirs) - kwargs.get('limited')) ]:
            client.containers.get(os.getenv('CONTAINER_NAME')).exec_run(
                'rm -rf %s' % d.replace(
                    kwargs.get('origin_db_path'), 
                    kwargs.get('docker_db_path')
                )
            ) if use_docker else shutil.rmtree(d, ignore_errors=True, onerror=True)  

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-m", "--mode", dest="mode", help="use backup mode", default=Constant.Mode.MONGO)
    parser.add_option(
        "-i", "--in", dest="in_path", help="location directory use to backup", default='.')
    parser.add_option(
        "-o", "--out", dest="out_path",
        help="output folder/file for backup", default="/tmp")
    parser.add_option(
        "--docker_out", dest="docker_out_path",
        help="output folder/file for backup in docker", default="/tmp")
    parser.add_option(
        "-H", "--host", dest="host",
        help="which http server to use", default="mongodb://localhost:27017")
    parser.add_option(
        "-n", "--number", dest="number",
        help="Limited number of backups", default=5)
    parser.add_option(
        "-d", "--database", dest="database",
        help="dump from database", default=None)
    parser.add_option(
        "-c", "--collection", dest="collection",
        help="dump from collection", default=None)
    parser.add_option(
        "-f", "--format", dest="format",
        help="name format of file/folder backup", default=None)
    parser.add_option(
        "--rsync", dest="rsync",
        help="use rsync mode", default=False)

    (options, args) = parser.parse_args(sys.argv)
    out_path = '%s/%s' % (options.docker_out_path if use_docker else options.out_path , 
                          datetime.datetime.now().strftime( options.format if 
                                                  options.format 
                                                  else '%Y-%m-%d_%H:%M:%s'))


    limited_process(get_lists(options.out_path), 
                    origin_db_path=options.out_path, 
                    docker_db_path=options.docker_out_path, 
                    limited=int(os.getenv('LIMITED')) or 5)

    if options.mode == Constant.Mode.MONGO:
        backup_with_mongodump(options.host, options.database, options.collection, out_path)
    elif options.mode == Constant.Mode.CP:
        backup_with_cp(options.in_path, out_path, rsync=True if options.rsync else False)
