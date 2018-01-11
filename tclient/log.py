# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""为 tclient 提供日志支持

tclient 使用三种 logger：
- monitor: 记录系统监控部分的日志和重大变更.
- scheduler: 记录排程的运行情况.
- job: 记录排程中的每个 Job 的运行情况.要注意的是 每个 Job 可能都有自己单独的日志文件i.
"""


import logging
import logging.handlers as handlers
import os.path
from tclient.config import root_dir


class DefaultFormatter(logging.Formatter):
    """tclient 中的日志格式化器.

    继承自 logging.Formatter"""
    DEFAULT_FORMAT = '[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)


class DefaultHandler(handlers.TimedRotatingFileHandler):
    """tclient 中的日志 handler

    必须传入 文件名
    """

    DEFAULT_WHEN = 'd'
    DEFAULT_COUNT = 14
    DEFAULT_INTERVAL = 1

    def __init__(self,
                 filename,
                 when=DEFAULT_WHEN,
                 interval=DEFAULT_INTERVAL,
                 backup_count=DEFAULT_COUNT,
                 encoding='utf-8'):
        handlers.TimedRotatingFileHandler.__init__(self,
                                                   filename,
                                                   when=when,
                                                   interval=interval,
                                                   backupCount=backup_count,
                                                   encoding=encoding)
        self.setLevel(logging.DEBUG)
        self.setFormatter(DefaultFormatter())


def construct_logger(name):
    """传入名称，返回 logger"""

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(DefaultHandler(os.path.join(root_dir, name, name)))
    return logger


mon_log = construct_logger('monitor')
sched_log = construct_logger('scheduler')
job_log = construct_logger('job')
