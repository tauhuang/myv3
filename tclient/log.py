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
import shutil
import time
from tclient.config import ROOT_DIR
from tclient.util import to_unicode, mkdir_not_exists


_BASE_LOGDIR = os.path.join(ROOT_DIR, 'log')


class DefaultFormatter(logging.Formatter):
    """tclient 中的日志格式化器.

    继承自 logging.Formatter"""
    DEFAULT_FORMAT = '[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self, fmt=DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)


class DefaultFileHandler(handlers.BaseRotatingHandler):
    """keep_days 日志保留天数，如果为 0 则永久保留，默认保留 7 天"""
    def __init__(self, filename, keep_days=7):
        handlers.BaseRotatingHandler.__init__(self,
                                              filename=filename,
                                              mode='a',
                                              encoding='utf-8')
        # 日志完整名称为 tclient 根目录/log/日期/filename
        self.baseFilename = os.path.join(_BASE_LOGDIR,
                                         time.strftime('%Y%m%d', time.localtime()),
                                         filename)
        self._keep_days = keep_days
        self.setLevel(logging.DEBUG)
        self.setFormatter(DefaultFormatter())

    def _open(self):
        # 新增功能： 如果路径不存在，则创建对应的目录.
        # 重构从 logging.FileHandler 类继承的 _open 方法

        log_dir = os.path.dirname(self.baseFilename)
        mkdir_not_exists(log_dir)
        return handlers.BaseRotatingHandler._open(self)

    def shouldRollover(self, record):
        pass

    def get_logdir_to_delete(self):
        pass

    def doRollover(self):
        dir_named_date = time.strftime('%Y%m%d', time.localtime())
        self.baseFilename = os.path.join(_BASE_LOGDIR, dir_named_date, os.path.basename(self.baseFilename))
        if self._keep_days > 0:
            for s in self.get_logdir_to_delete():
                shutil.rmtree(s, ignore_errors=True)


def construct_logger(name):
    """传入名称，返回 logger"""

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(DefaultFileHandler(name+'.log'))
    return logger


mon_log = construct_logger('monitor')
sched_log = construct_logger('scheduler')
job_log = construct_logger('job')


def safe_logmsg(msg):
    try:
        return to_unicode(msg)
    except UnicodeDecodeError:
        return repr(msg)
