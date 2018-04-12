# -*- coding: UTF-8 -*-

from tclient.download import download
from tclient.installupdate import update


import time


def install():
    download()
    time.sleep(60)
    update()