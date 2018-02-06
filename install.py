# -*- coding: UTF-8 -*-


import getpass
import os
import sys
try:
    from tclient import version
except ImportError:
    version = '3.0.0 beta'
import warnings


_ROOT_DIR = os.path.abspath(sys.argv[0])


def gen_release_file():
    release_file = os.path.join(_ROOT_DIR, 'release_version')
    try:
        with open(release_file, 'wt') as f:
            f.write('Version:'+ version)
    except IOError:
        warnings.warn("failed to create file '{0}'".format(release_file), UserWarning)


def gen_env_file():
    # only for Unix
    if sys.platform != 'linux':
        return

    cnf_path = os.path.join(_ROOT_DIR, 'conf')
    env_file = os.path.join(cnf_path, 'os_env')
    if not os.path.exists(cnf_path):
        try:
            os.mkdir(cnf_path)
        except IOError:
            raise SystemExit('Failed to mkdir {0}'.format(cnf_path))
    try:
        with open(env_file, 'wt') as f:
            f.write("# os user's system environments")
    except IOError:
        raise SystemExit('Failed to write something to file {0}'.format(env_file))
    with open(env_file, 'at') as f:
        for var, val in os.environ.iteritems():
             f.write('export {0}={1}'.format(var, val))


if __name__ == '__main__':
    if getpass.getuser() != "tiptop":
        raise SystemExit("Use user 'tiptop' to run")

    gen_release_file()
    gen_release_file()


