#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/5 16:05
@Author : Jocx-H
@File   : info_dao.py
@Desc   :  PyCharm
'''

import traceback

from typing import List
from dao.utils import client

info = client.test.info_new


def getMovies(movie_list: List[str]):
    r"""
    根据movieid列表查询对应电影的信息
    :return:
    """
    con = [{'id': int(i)} for i in movie_list]
    res = []
    try:
        minfo = info.find({'$or': con}, {'_id': 0, 'id': 1, 'name': 1, 'url': 1})
        for i in minfo:
            res.append(i)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        return None
    return res


if __name__ == '__main__':
    ll2 = ['190305', '136503', '168252', '132888', '5060', '189363', '158254', '148626', '159435', '152081', '140076',
           '148626']
    res = getMovies(ll2)
    print(len(res), res)
