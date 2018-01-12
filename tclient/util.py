# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Digiwin Inc.
#


"""提供一些工具性函数和类"""


import hashlib
import os.path
import subprocess
from threading import Lock
from ConfigParser import SafeConfigParser

try:
    from collections import OrderedDict as default_dict
except ImportError:
    # fallback for setup.py which hasn't yet built _collections
    default_dict = dict


class MyConfigParser(SafeConfigParser):
    """继承 SafeConfigParser ，新增一个 commit() 方法，用于将改变的配置内容写入配置文件"""

    write_lock = Lock()  # 写入锁， 同时只允许一个线程进行配置文件写入操作

    def __init__(self, defaults=None, dict_type=default_dict, allow_no_value=False):
        SafeConfigParser.__init__(self, defaults, dict_type, allow_no_value)
        self._config_filename = None  # 打开并解析的配置文件名

    def read(self, filenames):
        config_files = SafeConfigParser.read(self, filenames)
        self._config_filename = config_files[0]
        return config_files

    def commit(self):
        """将变动的配置内容，写入到配置文件中"""

        with MyConfigParser.write_lock:
            with open(self._config_filename, "w") as fp:
                SafeConfigParser.write(self, fp)


def run_cmd(cmd_str):
    """执行 Linux Shell 命令

    Arg: cmd_str 字符串， 要执行的命令
    Return: Shell 命令的 exit code, stdout, stderr
    大多数命令正常执行完，stderr 为空

    returncode, stdout, stderr = run_cmd('ls -l')"""

    p = subprocess.Popen(cmd_str, shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr


def merge_dicts(*args):
    """将多个 dict 合并为一个 dict

    Arg： 一个或多个 dict
    Return： dict
    Exception: 如果传入参数不为字典则引起 ValueError"""

    if not args:
        return {}
    merged_dict = {}
    for i in args:
        if isinstance(i, dict):
            merged_dict.update(i)
        else:
            pass
    return merged_dict


def convert_unicode_to_str(data, ignore_dicts=False):
    """将一个 Unicode 或 list、dict 的 Unicode 成员转换为 str """

    if not isinstance(data, (basestring, unicode, list, dict)):
        raise ValueError
    if isinstance(data, unicode):
        return data.encode('utf-8')
    if isinstance(data, list):
        return [convert_unicode_to_str(item, ignore_dicts=True) for item in data]
    if isinstance(data, dict) and not ignore_dicts:
        return {convert_unicode_to_str(key, ignore_dicts=True): convert_unicode_to_str(value)
                for (key, value) in data.iteritems()}
    return data


def to_unicode(string):
    """将一个字符串转换为 Unicode. 如果传入值不为字符串则引起 TypeError 错误."""

    base_str = (basestring, type(None))
    base_unicode = (unicode, type(None))
    if isinstance(string, base_unicode):
        return string
    if not isinstance(string, base_str):
        raise TypeError("Expected str, unicode, or None; got {0}".format(type(string)))
    return string.decode('utf-8')


def cal_md5(filename):
    """返回文件的 MD5 校验码"""

    if not os.path.exists(filename):
        raise IOError('{0} not exists'.format(filename))
    if not os.path.isfile(filename):
        raise ValueError('{0} is not a file'.formate(filename))

    md5obj = hashlib.md5()
    try:
        with open(filename, 'rb') as f:
            md5obj.update(f.read())
    except IOError as i:
        raise i("failed to read {0}".format(filename))
    except Exception:
        raise Exception('failed to calculate md5')

    return md5obj.hexdigest()
