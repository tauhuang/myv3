# -*- coding: UTF-8 -*-


import time
from tclient.log import mon_log
from tclient.util import run_cmd


def monitor_scheduler():
    cmd = 'ps -ef |grep tclient|grep schedule|wc -l'
    returncode, stdout, stderr = run_cmd(cmd)
    if returncode != 0:
        mon_log('monitor_scheduler: run "{0}", stderr: {1}, stdout:{2}.'.format(cmd, stderr, stdout))
    if int(stdout) == 0:
        pass #start schedule
    elif int(stdout) > 1:
        pass # stop all schedule and start schedule
    else:
        pass


def main():
    while True:
        monitor_scheduler()
        time.sleep(300)
