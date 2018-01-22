# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import datetime
import os
import re
import requests
from config import safe_baseurl, get_erp_lic
from tclient.log import job_log, _DATE_FORMAT, _BASE_LOGDIR
from tclient.util import cal_file_md5


def return_log_path():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return os.path.join(_BASE_LOGDIR, yesterday.strftime(_DATE_FORMAT))


def return_files():
    # return a list obtain full path file name
    log_path = return_log_path()
    return [os.path.join(_BASE_LOGDIR, i) for i in os.listdir(log_path)]


def get_filemd5(filename):
    try:
        return cal_file_md5(filename)
    except Exception:
        job_log.exception('calculate the md5 key of file "{0}"'.format(filename))
        return ''


def response_ok(response):
    if not response.ok:
        job_log.warning('id: {0}, request: {1}, response: code: {2}, reason: {3}, message {4}'.format(
            _LOG_ID, response.request, response.status_code, response.reason, response.content))
        return False
    return True


def http_post(json_dict):
    url = '/'.join([safe_baseurl.base_url, 'uploadlog'])
    resend_num = 3
    while resend_num:
        resend_num -= 1
        r = requests.post(url=url, json=json_dict)
        if response_ok(r):
            break


def upload_file(filename):



def main():
    files = return_files(return_log_path())  # files is a list
    for f in files:
        upload_file(f)

