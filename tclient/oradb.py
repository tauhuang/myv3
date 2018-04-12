# -*- coding: UTF-8 -*-


try:
    import cx_Oracle
except ImportError as e:
    cx_Oracle = None
    _imp_errmsg = str(e)

from tclient.log import mon_log


"""导入后需要判断 cx_Oracle"""


class SQLError(Exception):
    pass


def check_cxora():
    if cx_Oracle is None:
        mon_log.error('failed to "import cx_Oracle", exception message: {0}.'.format(_imp_errmsg))
        return False
    return True


def verify_conn(user, passwd, inst_name):
    """确认使用给定的账户、密码、instance_id 是否能登陆，能登陆返回 True，反之返回 False"""

    if not check_cxora():
        return False

    if user == 'sys':
        login_mode = cx_Oracle.SYSDBA
    else:
        login_mode = 0

    try:
        with cx_Oracle.Connection(user, passwd, inst_name, mode=login_mode):
            pass
        return True
    except cx_Oracle.DatabaseError:
        return False
    except cx_Oracle.Error as err:
        mon_log.error('failed to connect to Oracle DB, exception message: {0}.'.format(str(err)))
        return False


def exe_sql(user, passwd, inst_name, sql_str):
    """只执行查询 SEELCT SQL语句. 执行有异常， 则抛出 SQLError， 正常执行则返回查询结果"""
    if not check_cxora():
        raise SQLError(_imp_errmsg)

    if user == 'sys':
        login_mode = cx_Oracle.SYSDBA
    else:
        login_mode = 0

    try:
        with cx_Oracle.Connection(user, passwd, inst_name, mode=login_mode) as conn:
            cursor = conn.cursor()
            for row in cursor.execute(sql_str):
                # row is a tuple
                yield row
    except cx_Oracle.DatabaseError as err:
        raise SQLError(str(err))
