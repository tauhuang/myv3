# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import base64
import datetime
import os
import requests
import uuid
from config import safe_baseurl, erp_license, ROOT_DIR
from tclient.log import job_log, DATE_FORMAT, BASE_LOGDIR
from tclient.util import cal_file_md5, mkdir_not_exists, compress_file


_LOG_ID = uuid.uuid4()


class LogData(object):
    def __init__(self, erplicense=erp_license):
        self._erplic = erplicense
        self._md5 = None
        self._filename = None
        self._logdate = None
        self._base64string = None

    def _construct(self, attr_name):
        if hasattr(self, attr_name) and not (self.__dict__[attr_name] is None):
            return self.__dict__[attr_name]
        else:
            return ''

    @property
    def erplicense(self):
        return self._erplic

    @property
    def md5(self):
        return self._construct('_md5')

    @md5.setter
    def md5(self, md5_str):
        self._md5 = md5_str

    @property
    def filename(self):
        return self._construct('_filename')

    @filename.setter
    def filename(self, file_name):
        self._filename = file_name

    @property
    def logdate(self):
        return self._construct('_logdate')

    @logdate.setter
    def logdate(self, logdate_str):
        # format: 20180105
        self._logdate = logdate_str

    @property
    def base64string(self):
        return self._construct('_base64string')

    @base64string.setter
    def base64string(self, base64_str):
        self._base64string = base64_str

    @property
    def json(self):
        return {
            "erpLic": self.erplicense,
            "md5": self.md5,
            "fileName": self.filename,
            "logDate": self.logdate,
            "base64String": self.base64string
        }


_logdata = LogData()


def return_log_path():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return os.path.join(BASE_LOGDIR, yesterday.strftime(DATE_FORMAT))


def return_files():
    # return a list obtain full path file name
    log_path = return_log_path()
    return [os.path.join(log_path, i) for i in os.listdir(log_path)]


def return_compressed_files():
    files = return_files()
    tempdir = os.path.join(ROOT_DIR, 'tmp')
    mkdir_not_exists(tempdir)
    compressed_files = []
    for f in files:
        try:
            compressed_filename = os.path.join(tempdir, os.path.basename(f)+'.gz')
            compress_file(f, compressed_filename)
            compressed_files.append(compressed_filename)
        except Exception:
            job_log.exception('id: {0}, Failed to compress log {1}'.format(_LOG_ID, f))

    return compressed_files


def get_filemd5(filename):
    try:
        return cal_file_md5(filename)
    except Exception:
        job_log.exception('id: {0}, calculate the md5 key of file "{1}"'.format(_LOG_ID, filename))
        return ''


def encode_file(filename):
    try:
        with open(filename, 'rb') as f:
            return base64.b64encode(f.read())
    except IOError:
        job_log.warning('id: {0}, failed to read file {1}'.format(_LOG_ID, filename))
        return ''


def response_ok(response, retry_no):
    if not response.ok:
        job_log.warning('id: {0}, Retry No: {1}, request: {2}, response: code: {3}, reason: {4}, message {5}'.format(
            _LOG_ID, retry_no, response.url, response.status_code, response.reason, repr(response.content)))
        return False
    return True


def http_post(json_dict):
    url = '/'.join([safe_baseurl.base_url, 'uploadlog'])
    retry_times = 3
    # if failed retry three times
    while retry_times:
        r = requests.post(url=url, json=json_dict)
        if response_ok(r, 3-retry_times):
            break
        retry_times -= 1


def upload(logdata=_logdata):
    file_list = return_compressed_files()
    logdata.logdate = os.path.basename(return_log_path())
    for f in file_list:
        logdata.filename = os.path.basename(f)
        logdata.md5 = cal_file_md5(f)
        logdata.base64string = encode_file(f)
        http_post(logdata.json)
        os.remove(f)
