# -*-: coding: UTF-8 -*-


import os.path
import sys


__all__ = ['pypath']


_path = os.path.dirname(os.path.abspath(sys.argv[0]))
_package_rootpath = os.path.dirname(os.path.dirname(_path))
pypath = sys.path.append(_package_rootpath)