# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import os.path
import requests
import uuid
from tclient import version
from tclient.config import ROOT_DIR, SafeBaseURL, DEFAULT_CONF, get_erp_lic
from tclient.log import job_log
from tclient.util import mkdir_not_exists, cal_file_md5, MyConfigParser


_BASE_URL = SafeBaseURL()
_LOG_ID = uuid.uuid4()


def response_ok(response):
    if not response.ok:
        job_log.warning('id: {0}, request: {1}, response: code: {2}, reason: {3}, message {4}'.format(
            _LOG_ID, response.request, response.status_code, response.reason, response.content))
        return False
    return True


def get_download_url():
    """返回更新包压缩文件包的 md5 校验值和下载 URL"""

    url = '/'.join([_BASE_URL.base_url, 'tclientDojson'])
    response = requests.get(url=url, params={'arg': version, 'erpLic': get_erp_lic()})
    if response_ok(response):
        response_body = response.json()
        return response_body['md5'], response_body['file'], response_body['url']
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
    md5key, filename, url = get_download_url()
    download_path = os.path.join(ROOT_DIR, 'download')
    mkdir_not_exists(download_path)

    if not (md5key and filename and url):
        job_log.warning('id: {0}, md5key: {1}, download url: {2}'.format(_LOG_ID, md5key, url))

    response = requests.get(url=url)
    if not response_ok(response):
        pass
    download_file = os.path.join(download_path, filename)
    try:
        with open(download_file, 'wb') as f:
            f.write(response.content)
        if not compare_md5(md5key, download_file):
            job_log.warning('id: {0}, the md5 key of update file not match the server gave'.format(_LOG_ID))
        notify_update(download_file)
    except IOError:
        job_log.warning('id: {0}, failed to write update file "{1}".'.format(_LOG_ID, download_file))
