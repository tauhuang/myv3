# -*- coding: UTF-8 -*-
# 获取 Linux 服务器的一些基本信息


import os.path
import platform
import psutil
import re
import socket
from multiprocessing import cpu_count
from tclient.config import ROOT_DIR
from tclient.util import merge_dicts, run_cmd


def get_ip_by_udp():
    ip = ''
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 用阿里云 DNS 来测试本机IP
        conn.connect(('223.5.5.5', 53))
        ip = conn.getsockname()[0]
    except Exception:
        pass
    finally:
        conn.close()
    return ip


def get_ip_by_cmd():
    cmd = 'hostname -I'
    returncode, stdout, _ = run_cmd(cmd)
    if returncode == 0:
        return stdout.split()[0]
    else:
        return ''


def get_ip():
    for ip in (get_ip_by_cmd(), get_ip_by_cmd()):
        if ip:
            return {"ip": str(ip)}
    return {"ip": ""}


def get_hostname():
    return {"hostName": platform.node()}


def read_biosfile(filename):
    try:
        with open(filename, "rt") as f:
            for line in f:
                if re.search("Product Name", line, flags=re.I):
                    prod = line.split(":")[1].strip()
                    f.close()
                    return {"serverType": prod}
    except IOError:
        return {"serverType": "failed to read file"}
    return {"serverType": "not found"}


def get_hdtype():
    files = ('/u1/etc/bios.data',
             os.path.join(os.path.expanduser('~'), 'bios.data'),
             os.path.join(ROOT_DIR, 'conf', 'bios.data'))
    for f in files:
        if os.path.exists(f):
            return read_biosfile(f)
        else:
            return {"serverType": "file not found"}


def get_osdist():
    """Linux distribution"""
    osdist = " ".join(platform.linux_distribution()[0:2])
    return {"os": osdist}


def get_cpucount():
    return {"cpuCount": str(cpu_count())}


def get_ram():
    ramsize_in_gb = psutil.virtual_memory().total / 1024.0 / 1024.0 / 1024.0
    ramsize_in_gb = str(int(round(ramsize_in_gb, 0)))
    return {"ram": ramsize_in_gb}


def get_swap():
    swapsize_in_gb = psutil.swap_memory()[0] / 1024.0 / 1024.0 / 1024.0
    swapsize_in_gb = str(int(round(swapsize_in_gb, 0)))
    return {"swap": swapsize_in_gb}


def get_cputype():
    with open("/proc/cpuinfo", "rt") as f:
        for line in f:
            if re.search("model name", line, flags=re.I):
                cpu_type = line.split(":")[1].strip()
                return {"cpuType": cpu_type}


def get_data():
    return merge_dicts(get_ip(),
                       get_hostname(),
                       get_hdtype(),
                       get_osdist(),
                       get_cpucount(),
                       get_ram(),
                       get_swap(),
                       get_cputype())
