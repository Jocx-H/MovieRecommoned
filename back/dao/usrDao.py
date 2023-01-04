#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/4 20:03
@Author : Jocx-H
@File   : usrDao.py
@Desc   :  PyCharm
'''


import traceback

from typing import Dict
from dao.utils import client


usr = client.test.usr


def getUsr(_u: str):
    r"""
    根据哈希后的用户结果获取用户。
    :param _u:  哈希后的用户名
    """
    res = []
    try:
        utemp = usr.find({'usrId': _u}, {'_id': 0})
        for i in utemp:
            res.append(i)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        return None
    return res