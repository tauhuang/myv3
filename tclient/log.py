# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""为 tclient 提供日志支持

tclient 使用三种 logger：
- tclient.monitor: 记录系统监控部分的日志和重大变更.
- tclient.scheduler: 记录排程的运行情况.
- tclient.job: 记录排程中的每个 Job 的运行情况.要注意的是 每个 Job 可能都有自己单独的日志文件i.
"""


import logging
import logging.handlers


mon_log = logging.getLogger('tclient.monitor')
sched_log = logging.getLogger('tclient.scheduler')
app_log = logging.getLogger('tclient.job')


class LogFormatter(logging.Formatter):
    """tclient 中的日志格式化器.

    继承自 logging.Formatter"""
    DEFAULT_FORMAT = '[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)
