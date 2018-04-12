# -*- coding: UTF-8 -*-


from tclient.util import merge_dicts


def get_dprole():
    """去人本服务器部署角色是 AP or ALL or APN.

        AP: 只做AP服务器.
        ALL: AP + DB.
        APN: AP + RAC 其中一个节点."""

    return {"deployStatus": ""}


def get_rac_nodes():
    """是否为RAC， 如果为RAC 节点数是多少. 返回 'N' 或者 数字"""

    return {"rac": ""}


def get_data():
    return merge_dicts(get_dprole(), get_rac_nodes())