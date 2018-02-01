# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""解压更新包，并执行更新包中的脚本 update.py"""


import imp
import os.path
import shutil
import tarfile
import uuid

#导入更新包解压后的安装程序 install_update.py
try:
    imp.load_source() install_update
except ImportError:
    install_update = None

from tclient.config import ROOT_DIR, DEFAULT_CONF
from tclient.feedback import feedback
from tclient.log import mon_log
from tclient.util import MyConfigParser, mkdir_not_exists


_LOG_ID = uuid.uuid4()
_TMPDIR = os.path.join(ROOT_DIR, 'tmp')
_BACKUP_DIR = os.path.join(ROOT_DIR, 'backup')
_BACKUP_LIST = [os.path.join(ROOT_DIR, 'tclient'),
                os.path.join(ROOT_DIR, 'conf'),
                os.path.join(ROOT_DIR, 'db')]


def backup():
    shutil.rmtree(_BACKUP_DIR)
    mkdir_not_exists(_BACKUP_DIR)
    for i in _BACKUP_LIST:
        shutil.move(i, os.path.join(_BACKUP_DIR, os.path.basename(i)))


def uncompress(tarfilename):
    mkdir_not_exists(_TMPDIR)
    if os.path.exists(tarfilename):
        try:
            t = tarfile.open(tarfilename, 'r')
            t.extractall(_TMPDIR)
            return True
        except Exception:
            mon_log.error('id: {0}, failed to extract {1}'.format(_LOG_ID, tarfilename))
    else:
        mon_log.error('id: {0}, {1} not found'.format(_LOG_ID, tarfilename))
    return False


def disbale_update_prep():
    cnf = MyConfigParser()
    cnf.read(DEFAULT_CONF)
    cnf.set('update', 'prepare', 'N')
    cnf.set('update', 'file', '')
    cnf.commit()


def update():
    cnf = MyConfigParser()
    cnf.read(DEFAULT_CONF)
    compress_ok = False
    if cnf.get('update', 'prepare') == 'Y':
        filename = cnf.get('update', 'file')
        if filename:
            compress_ok = uncompress(filename)
        else:
            mon_log.error('id : {0}, tarfilename is empty'.format(_LOG_ID))
    disbale_update_prep()
    if not compress_ok:
        feedback('failed', 'installation', _LOG_ID)

    if install_update:
        # 返回是否成功的 Bool 值 和 log_id， 如果返回 True， 则 log_id 为空字符串
        try:
            install_update.run()
        except Exception:
            mon_log.error('id: {0}, failed to install update'.format(_LOG_ID))
            feedback('failed', 'installation', _LOG_ID)
