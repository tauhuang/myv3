# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import requests
from tclient import version


def send_get_requests():
    r = requests.get(url='http://172.16.101.43/wstopprd/ws/r/tclientDojson', params={'arg': version})
