# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


import datetime
import os
from log import _DATE_FORMAT, _BASE_LOGDIR


def return_log_path():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return os.path.join(_BASE_LOGDIR, yesterday.strftime(_DATE_FORMAT))


def return_files():
    # return a list obtain full path file name
    log_path = return_log_path()
    return [os.path.join(_BASE_LOGDIR, i) for i in os.listdir(log_path)]
