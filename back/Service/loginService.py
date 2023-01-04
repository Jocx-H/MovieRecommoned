#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/4 20:09
@Author : Jocx-H
@File   : loginService.py
@Desc   :  PyCharm
'''


import json
import random
import traceback

from hashlib import md5
from typing import Dict
from dao import usrDao


def __compare__(u):
    try:
        usr_hash = md5()
        usr_hash.update(u.encode(encoding='utf-8'))
        _u = usr_hash.hexdigest()
        usr = usrDao.getUsr(_u)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise e
    if len(usr) != 1:
        return False
    return True


def isLogin(usr) -> Dict:
    return {'result': __compare__(usr)}


if __name__ == '__main__':
    print(__compare__('Jocx'))
    print(__compare__('1'))
    print(__compare__('sdf'))
    print(__compare__('10532'))