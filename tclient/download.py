# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import os.path
import requests
import uuid
from tclient import version
from tclient.config import ROOT_DIR, safe_baseurl, DEFAULT_CONF, erp_license
from tclient.feedback import feedback
from tclient.log import mon_log, safe_logmsg
from tclient.util import mkdir_not_exists, cal_file_md5, MyConfigParser


_LOG_ID = uuid.uuid4()


def response_ok(response):
    if not response.ok:
        mon_log.warning(
            safe_logmsg(
                'id: {0}, request_url: {1}, response: code: {2}, reason: {3}, message {4}'.format(
                    _LOG_ID, response.url, response.status_code, response.reason, repr(response.content)
                )
            )
        )
        return False
    return True


def has_update(response_body):
    updatestat = response_body['update']
    if isinstance(updatestat, basestring):
        return updatestat.upper() == u'Y'
    else:
        mon_log.warning(
            safe_logmsg(
                'id: {0}, response key "update" value is not string type, value is {1} type: {2}'.format(
                    _LOG_ID, updatestat, type(updatestat)
                )
            )
        )
        return False


def get_download_url(version, erp_license):
    """返回更新包压缩文件包的 md5 校验值和下载 URL"""

    url = '/'.join([safe_baseurl.base_url, 'updateprog'])
    response = requests.get(url=url, params={'version': version, 'erpLic': erp_license})
    if response_ok(response):
        response_body = response.json()
        if has_update(response_body):
            try:
                url, md5, filename = response_body[u'url'], response_body[u'md5'], response_body[u'filename']
                return url, md5, filename
            except KeyError:
                mon_log.exception('not found key in response json')
    return '', '', ''


def compare_md5(md5key, filename):
    return md5key == cal_file_md5(filename)


def notify_update(filename):
    cnf = MyConfigParser()
    cnf.read(DEFAULT_CONF)
    if not cnf.has_section('update'):
        cnf.add_section('update')
    cnf.set('update', 'prepare', value='Y')
    cnf.set('update', 'file', value=filename)
    cnf.commit()


def download_zip():
    url, md5key, filename = get_download_url(version, erp_license)
    download_path = os.path.join(ROOT_DIR, 'download')
    mkdir_not_exists(download_path)

    if not (md5key and filename and url):
        mon_log.warning('id: {0}, md5key: {1}, download url: {2}'.format(_LOG_ID, md5key, url))
        return False

    response = requests.get(url=url)
    if not response_ok(response):
        return False
    download_file = os.path.join(download_path, filename)
    try:
        with open(download_file, 'wb') as f:
            f.write(response.content)
        if not compare_md5(md5key, download_file):
            mon_log.warning('id: {0}, the md5 key of update file not match the server gave'.format(_LOG_ID))
        notify_update(download_file)
        return True
    except IOError:
        mon_log.warning('id: {0}, failed to write update file "{1}".'.format(_LOG_ID, download_file))
        return False

def download():
    if not download_zip():
        feedback(status='failed', reason='download', log_id=str(_LOG_ID))
