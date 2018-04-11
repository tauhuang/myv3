# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import os.path
import re


# root dir 是 config.py 所在路径的父目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
BASE_URL = 'http://172.16.101.43/wstopprd/ws/r'
# BASE_URL = 'http://122.146.130.244:8081/tclient/v1'
DEFAULT_CONF = os.path.join(ROOT_DIR, 'conf', 'tclient.cnf')


class ERPLicense(object):
    """T100 ERP License Number"""

    def __init__(self):
        self._license = self._get_lic()

    @property
    def license(self):
        return self._license

    @license.setter
    def license(self, lic_no):
        try:
            self.license = str(lic_no).upper()
        except Exception:
            self.license = repr(lic_no).upper()

    def _get_lic(self):
        lic_file = "/u1/topkey/reg.cfg"
        pattern = "License"
        try:
            with open(lic_file, 'rt') as f:
                for line in f:
                    if re.search(pattern, line, flags=re.I):
                        lic_no = line.split("=")[1].strip()
                        return lic_no
        except IOError:
            return ""
        return ""


erp_license = ERPLicense().license
