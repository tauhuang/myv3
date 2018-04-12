# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""解压更新包，备份原程序，执行更新包中的脚本 update.py, 若脚本执行异常，则回滚备份的程序"""


import os.path
import shutil
import tarfile
import uuid
from tclient.config import ROOT_DIR, DEFAULT_CONF
from tclient.feedback import feedback
from tclient.log import mon_log
from tclient.util import MyConfigParser, mkdir_not_exists, run_cmd


_LOG_ID = uuid.uuid4()
_UPDATE_TMP = os.path.join(ROOT_DIR, 'tmp', 'update')
_BACKUP_DIR = os.path.join(ROOT_DIR, 'backup')
_BACKUP_LIST = (os.path.join(ROOT_DIR, 'tclient'), os.path.join(ROOT_DIR, 'conf'))


def backup():
    try:
        shutil.rmtree(_BACKUP_DIR)
    except OSError:
        pass
    mkdir_not_exists(_BACKUP_DIR)
    for i in _BACKUP_LIST:
        shutil.copytree(i, os.path.join(_BACKUP_DIR, os.path.basename(i)))


def uncompress(tarfilename):
    try:
        shutil.rmtree(_UPDATE_TMP)
    except OSError:
        pass

    mkdir_not_exists(_UPDATE_TMP)
    if os.path.exists(tarfilename):
        try:
            t = tarfile.open(tarfilename, 'r')
            t.extractall(_UPDATE_TMP)
            return True
        except Exception:
            mon_log.error('id: {0}, failed to extract {1}'.format(_LOG_ID, tarfilename))
    else:
        mon_log.error('id: {0}, {1} not found'.format(_LOG_ID, tarfilename))
    return False


def rollback():
    for i in _BACKUP_LIST:
        try:
            shutil.rmtree(i)
            shutil.move(os.path.join(_BACKUP_DIR, os.path.basename(i)), ROOT_DIR)
        except OSError:
            pass




def update():
    cnf = MyConfigParser()
    cnf.read(DEFAULT_CONF)
    compress_ok = False
    if not cnf.has_section('update'):
        return

    if cnf.get('update', 'prepare') == 'Y':
        filename = cnf.get('update', 'file')
        if filename:
            compress_ok = uncompress(filename)
        else:
            mon_log.error('id : {0}, tarfilename is empty'.format(_LOG_ID))
    if not compress_ok:
        feedback('failed', 'installation', str(_LOG_ID))
        return

    # 备份原程序
    try:
        backup()
    except Exception as e:
        mon_log.error('id: {0}, backup failed.  exception message: {1}'.format(_LOG_ID, str(e)))
        feedback('failed', 'installation', str(_LOG_ID))
        return

    # 执行更新包中的 update.py 脚本
    cmd_str = os.path.join(ROOT_DIR, 'run') + ' ' + _UPDATE_TMP + 'tclient/update.py'
    returncode, stdout, stderr = run_cmd(cmd_str)
    if returncode != 0:
        mon_log.error('id: {0}, run update.py error, message: stderr: {1}, stdout: {2}'.format(_LOG_ID, stderr, stdout))
        try:
            rollback()
        except Exception as e:
            mon_log.error('id: {0}, rollback failed.  exception message: {1}'.format(_LOG_ID, str(e)))
        feedback('failed', 'installation', str(_LOG_ID))
