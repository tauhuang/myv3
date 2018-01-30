# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""发送客户端的更新情况"""


import requests
import time
import uuid
from tclient import version
from tclient.config import safe_baseurl, erp_license
from tclient.log import job_log, safe_logmsg


URL = '/'.join([safe_baseurl.base_url, 'updatestatus'])
_LOG_ID = uuid.uuid4()
_CURRENT_TIME = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())



class Data(object):
    """必须传入 status 的值,值为 success 或 faild. 若 status 为 faild 则需要传入 reason 和 log_id"""

    def __init__(self,
                 status,
                 erp_lic=erp_license,
                 tclient_ver=version,
                 update_time=_CURRENT_TIME,
                 reason=None,
                 log_id=None):

        self._json = {
            "erpLic": erp_lic,
            "tclientVer": tclient_ver,
            "updateTime": update_time,
            "status": status,
        }
        if status.lower() == "failed":
            self._json["reason"] = reason
            self._json["logId"] = log_id

    @property
    def json(self):
        return self._json


class HTTPPoster(object):
    """必须传入需要上传的 json 数据"""

    def __init__(self, json, url=URL):
        self.url = url
        self.json = json
        self.retry = 3

    def _post(self):
        self.response = requests.post(url=self.url, json=self.json)

    def post(self):
        while self.retry:
            self._post()
            if self.success:
                break
            self.retry -= 1

    @property
    def success(self):
        if not self.response.ok:
            job_log.warning(
                safe_logmsg(
                    'id: {0}, retry NO: {1}, request_url: {2}, response: code: {3}, reason: {4}, message {5}'.format(
                        _LOG_ID, 3-self.retry, self.response.url, self.response.status_code, self.response.reason,
                        self.response.content
                    )
                )
            )
            return False
        return True


def feedback(status, reason=None, log_id=None):
    json_data = Data(status=status, reason=reason, log_id=log_id)
    http_poster = HTTPPoster(json_data.json)
    http_poster.post()
