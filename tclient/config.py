# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


ROOT_DIR = ''
BASE_URL = 'http://172.16.101.43/wstopprd/ws/r'


class SafeBaseURL(object):
    def __init__(self):
        self._base_url = BASE_URL

    @property
    def base_url(self):
        url = self._base_url.lstrip('http://')
        url = url.replace('//', '/')
        url = ''.join('http://', url)
        return url.rstrip('/')

    @base_url.setter
    def base_url(self, value):
        if not isinstance(value, basestring):
            raise TypeError('base_url expected a string, you gave a {0}'.format(type(value)))
        self._base_url = value
