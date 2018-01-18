# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""为 tclient 提供日志支持

tclient 使用三种 logger：
- monitor: 记录系统监控部分的日志和重大变更.
- scheduler: 记录排程的运行情况.
- job: 记录排程中的每个 Job 的运行情况.要注意的是 每个 Job 可能都有自己单独的日志文件.

每次调用 logger 的 debug, warning, error 等日志信息接口时，都要先调用 safe_logmsg(),
以防止非 ASCII 字符串出现编码错误.
例子：
from tclient.log import mon_log

mon_log.debug(safe_logmsg('时间 %s' % '不确定')
"""


import logging
import logging.handlers as handlers
import os
from tclient.config import ROOT_DIR
from tclient.util import to_unicode, mkdir_not_exists


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

    def _open(self):
        # 新增功能： 如果路径不存在，则创建对应的目录.
        # 重构从 logging.FileHandler 类继承的 _open 方法

        log_dir = os.path.dirname(self.baseFilename)
        mkdir_not_exists(log_dir)
        return handlers.TimedRotatingFileHandler._open(self)


class DefaultFileHandler(handlers.RotatingFileHandler):
    """tclient 中日志 handler, 继承自 logging.handlers.RotatingFileHandler

    必须传入文件名 filename. 日志文件会存在于 tclient 根目录下的 log 下的 以当前日期（格式20180105)命名的目录下.
    例如: tclient 根目录是 /u1/usr/tiptop， 那么当前日志文件的完整路径是 /u1/usr/tiptop/tclient/log/20180105/job.log"""

    def __init__(self, filename, max_bytes=0, backup_count=0, encoding='utf-8'):
        handlers.RotatingFileHandler.__init__(self,
                                              filename=filename,
                                              maxBytes=max_bytes,
                                              backupCount=backup_count,
                                              encoding=encoding)
        self.setLevel(logging.DEBUG)
        self.setFormatter(DefaultFormatter())

    def _open(self):
        # 新增功能： 如果路径不存在，则创建对应的目录.
        # 重构从 logging.FileHandler 类继承的 _open 方法

        log_dir = os.path.dirname(self.baseFilename)
        mkdir_not_exists(log_dir)
        return handlers.RotatingFileHandler._open(self)

    def shouldRollover(self, record):
        pass

    def doRollover(self):
        pass


def construct_logger(name):
    """传入名称，返回 logger"""

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(DefaultHandler(os.path.join(ROOT_DIR, 'log', name+'.log')))
    return logger


mon_log = construct_logger('monitor')
sched_log = construct_logger('scheduler')
job_log = construct_logger('job')


def safe_logmsg(msg):
    try:
        return to_unicode(msg)
    except UnicodeDecodeError:
        return repr(msg)
