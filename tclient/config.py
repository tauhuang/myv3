# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import re
import os.path


ROOT_DIR = ''
BASE_URL = 'http://172.16.101.43/wstopprd/ws/r'
DEFAULT_CONF = os.path.join(ROOT_DIR, 'conf', 'tclient.cnf')


class SafeBaseURL(object):
    def __init__(self):
        self._base_url = BASE_URL

    @property
    def base_url(self):
        url = self._base_url.lstrip('http://')
        url = url.replace('//', '/')
        url = ''.join(['http://', url])
        return url.rstrip('/')

    @base_url.setter
    def base_url(self, value):
        if not isinstance(value, basestring):
            raise TypeError('base_url expected a string, you gave a {0}'.format(type(value)))
        self._base_url = value


safe_baseurl = SafeBaseURL()


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
