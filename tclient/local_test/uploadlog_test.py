# -*- coding: UTF-8 -*-


from loadpackage import *
from tclient.uploadlog import LogData, upload


if __name__ == '__main__':
    logdata = LogData(erplicense='TDAAAADV')
    upload(logdata)
