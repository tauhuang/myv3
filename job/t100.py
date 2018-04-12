# -*-: UTF-8 -*-
# Author: HuangTao
# get informations about T100 ERP


import fnmatch
import os
import re
import shutil
import tempfile
import uuid
from tclient import version
from tclient.config import erp_license
from tclient.log import job_log
from tclient.util import run_cmd, merge_dicts


_LOG_ID = uuid.uuid4()


def get_erp_lic():
    return {"t100Lic": erp_license}


def get_t100_ver():
    if os.getenv("TOP"):
        version_file = os.path.join(os.getenv("TOP"), "t100_release")
    else:
        return {"t100Ver": "file not found"}

    if not os.path.exists(version_file):
        return {"t100Ver": "file not found"}

    try:
        with open(version_file, "rt") as f:
            for line in f:
                if re.search("v", line, flags=re.I):
                    t_ver = line.strip()
                    f.close()
                    return {"t100Ver": t_ver}
    except IOError:
        return {"t100Ver": "failed to read file"}
    return {"t100Ver": "not found"}


def get_genero_ver(cmd_str):
    returncode, stdout, stderr = run_cmd(cmd_str)
    if returncode != 0:
        job_log.error("id: {0}, Execute unix command '{1}' failed, error message: {2}.".format(_LOG_ID, cmd_str, stderr))
        return "run command error"
    return stdout.split("\n")[0]


def get_fglrun_ver():
    cmd = "fglrun -V"
    return {"fglrunVer": get_genero_ver(cmd)}


def get_gas_ver():
    cmd = "fastcgidispatch -V"
    return {"gasVer": get_genero_ver(cmd)}


def get_flm_ver():
    cmd = ". $FLMDIR/envflm; flmprg -V"
    return {"flmprgVer": get_genero_ver(cmd)}


def get_fglwrt_ver():
    cmd = "fglWrt -V"
    return {"fglWrtVer": get_genero_ver(cmd)}


def get_gsform_ver():
    cmd = "gsform -V"
    return {"gsformVer": get_genero_ver(cmd)}


def get_tclient_ver():
    return {"tclientVer": version}


def get_gdcax_ver():
    if not os.getenv("FGLASDIR"):
        return {"gdcaxVer": "file not found"}

    tempdir = tempfile.mkdtemp()
    cab_file = os.path.join(os.getenv("FGLASDIR"), "web/fjs/activex/gdc.cab")
    cmd = " ".join(["cabextract -d", tempdir, cab_file])
    returncode, stdout, stderr = run_cmd(cmd)
    if returncode != 0:
        job_log.error("id: {0}, Execute unix command '{1}' failed, error message: {2}.".format(_LOG_ID, cmd, stderr))
        shutil.rmtree(tempdir, ignore_errors=True)
        return {"gdcaxVer": "run command error"}
    pattern = "*gdcax*.exe"
    for rootdir, dirs, files in os.walk(tempdir):
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                shutil.rmtree(tempdir, ignore_errors=True)
                return {"gdcaxVer": f.rstrip(".exe")}
    shutil.rmtree(tempdir, ignore_errors=True)
    return {"gdcaxVer": "not found"}


def get_t100_info():
    return merge_dicts(get_erp_lic(),
                       get_t100_ver(),
                       get_fglrun_ver(),
                       get_gas_ver(),
                       get_flm_ver(),
                       get_fglwrt_ver(),
                       get_gsform_ver(),
                       get_gdcax_ver(),
                       get_tclient_ver())
