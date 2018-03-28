# -*- coding: UTF-8 -*-


import schedule
from random import randint
from tclient.download import download
from tclient.installupdate import


def set_sched_time():
    # random time
    random_hour = randint(0, 23)
    random_minute = randint(0, 59)
    return ":".join(str(random_hour), str(random_minute))


def set_scheuler():
    pass