# -*- coding: UTF-8 -*-


import tempfile
from tclient.util import merge_dicts, run_cmd


"""用 Linux 的 dd 命令测试磁盘的写入速度"""


def get_dd_io():
    temp = tempfile.NamedTemporaryFile()
    cmd_str = "dd if=/dev/zero of=" + temp.name + " bs=8k count=200000"
    returncode, _, stderr = run_cmd(cmd_str)
    if returncode != 0:
        return {"io": ""}
    else:
        return {"io": stderr.splitlines()[2].split(",")[2].strip()}


def get_data():
    return get_dd_io()
