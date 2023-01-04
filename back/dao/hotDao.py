#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/4 17:03
@Author : Jocx-H
@File   : hotDao.py
@Desc   :  PyCharm
'''


import traceback

from typing import Dict
from dao.utils import client


hot = client.test.hot


def getHotMovieList():
    r"""
    获取默认情况下的热门电影列表。
    """
    res = []
    try:
        minfo = hot.find({}, {'_id': 0})
        for i in minfo:
            res.append(i)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        return None
    return res


if __name__ == '__main__':
    res = getHotMovieList()
    print(len(res), res)
