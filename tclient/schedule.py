# -*- coding: UTF-8 -*-


import time
from schedule import Scheduler
from random import randint
from tclient.downupdate import install
from tclient.uploadlog import upload
from job.send import send


def set_sched_time():
    # random time
    random_hour = randint(0, 8)
    random_minute = randint(0, 59)
    return ":".join(str(random_hour), str(random_minute))


def set_scheuler():
    sched = Scheduler()
    sched.every().day.at(set_sched_time()).do(upload)
    sched.every().day.at(set_sched_time()).do(install)
    sched.every().sunday.at(set_sched_time()).do(send)
    return sched


def main():
    scheduler = set_scheuler()
    while True:
        scheduler.run_pending()
        time.sleep(1)
