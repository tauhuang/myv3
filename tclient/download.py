# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import requests
from tclient import version
from tclient.config import BASE_URL


def send_get_requests():
    r = requests.get(url='/tclientDojson', params={'arg': version})
