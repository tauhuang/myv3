# -*- coding:UTF-8 -*-


from loadpackage import *
from tclient.log import job_log, safe_logmsg


def write_log():
    job_log.debug(safe_logmsg('时间'))
    job_log.error(safe_logmsg('错误 %s' % '编码错误'))
    job_log.critical(safe_logmsg('fatal： {0}'.format('系统崩溃')))


if __name__ == '__main__':
    write_log()
