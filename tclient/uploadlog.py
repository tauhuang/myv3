# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import base64
import datetime
import os
import requests
import uuid
from config import safe_baseurl, get_erp_lic
from tclient.log import job_log, DATE_FORMAT, BASE_LOGDIR
from tclient.util import cal_file_md5


_LOG_ID = uuid.uuid4()


def return_log_path():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return os.path.join(BASE_LOGDIR, yesterday.strftime(DATE_FORMAT))


def return_files():
    # return a list obtain full path file name
    log_path = return_log_path()
    return [os.path.join(BASE_LOGDIR, i) for i in os.listdir(log_path)]


def get_filemd5(filename):
    try:
        return cal_file_md5(filename)
    except Exception:
        job_log.exception('id: {0}, calculate the md5 key of file "{1}"'.format(_LOG_ID, filename))
        return ''


def response_ok(response, filename):
    if not response.ok:
        job_log.warning('id: {0}, request: {1}, response: code: {2}, reason: {3}, message {4}'.format(
            _LOG_ID, response.request, response.status_code, response.reason, response.content))
        return False
    status = response.json()['status']
    if status == u'notmatched':
        job_log.warning('id: {0}, the md5 key of file "{1}" not matched between client and server'.format(
                        _LOG_ID, filename))
    return True


def http_post(json_dict):
    url = '/'.join([safe_baseurl.base_url, 'uploadlog'])
    retry_times = 3
    # if failed retry three times
    while retry_times:
        retry_times -= 1
        r = requests.post(url=url, json=json_dict)
        if response_ok(r, json_dict['fileName']):
            break


def upload_file(filename):
    post_json = {
                 'erpLic': get_erp_lic(),
                 'md5': get_filemd5(filename),
                 'isEnd': 'N',
                 'fileName': os.path.basename(filename),
                 'logDate': os.path.basename(return_log_path())
                 }
    if post_json['md5']:
        try:
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(1024*1024*10)  # 10M each time
                    if chunk:
                        post_json['base64String'] = base64.b64encode(chunk)
                        http_post(post_json)
                    else:
                        post_json['base64String'] = ''
                        post_json['isEnd'] = 'Y'
                        break
        except IOError:
            job_log.error('id: {0}, failed to read log file {0}'.format(_LOG_ID, filename))
        except Exception:
            job_log.exception('id: {0}, failed to upload log file {0}'.format(_LOG_ID, filename))


def main():
    files = return_files()  # files is a list
    for f in files:
        upload_file(f)
