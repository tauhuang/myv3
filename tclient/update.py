# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#
# 离线更新


import os.path
import shutil
import tarfile
from tclient.config import ROOT_DIR, DEFAULT_CONF
from tclient.log import mon_log
from tclient.util import MyConfigParser, mkdir_not_exists


_UPDATE_DST = os.path.join(ROOT_DIR, 'tclient')
_ROLLBACK_PATH = os.path.join(ROOT_DIR, '.update_rollback')
_ROLLBACK_SRC = os.path.join(_ROLLBACK_PATH, os.path.basename(_UPDATE_DST))


def prepare():
    mkdir_not_exists(_ROLLBACK_PATH)


def backup_origin_file():
    shutil.move(_UPDATE_DST, _ROLLBACK_SRC)


def update_file(src_file):
    if os.path.exists(src_file):
        try:
            t = tarfile.open(src_file, 'r')
            t.extract(ROOT_DIR)
        except:
            mon_log.warning('failed to extract file "{0}"'.format(src_file))
    else:
        mon_log.warning('update file "{0} not exists'.format(src_file))


def update():
    cnf = MyConfigParser()
    cnf.read(DEFAULT_CONF)
    if cnf.get('update', 'prepare') == 'Y':
        update_file(cnf.get('update', 'file'))


def rollback():
    shutil.rmtree(_UPDATE_DST)
    shutil.move(_ROLLBACK_SRC, _UPDATE_DST)
