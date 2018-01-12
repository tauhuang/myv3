# -*- coding:UTF-8 -*-


from loadpackage import *
from tclient.log import mon_log, sched_log, job_log, safe_logmsg


if __name__ == '__main__':
    mon_log.debug(safe_logmsg('时间'))
    sched_log.error(safe_logmsg('错误 %s' % '编码错误'))
    job_log.critical(safe_logmsg('fatal： {0}'.format('系统崩溃')))