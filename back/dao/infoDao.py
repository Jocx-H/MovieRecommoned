#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/2 15:47
@Author : Jocx-H
@File   : infoDao.py
@Desc   :  PyCharm
'''

import traceback

from typing import Dict
from dao.utils import client


info = client.test.info_new


def getMovieDetails(movie_id: int):
    r"""
    获取一部电影的名字、类别、导演、简介、图片等详细信息
    :param movie_id: 电影自带的movie_id，不是数据库id
    """
    res = []
    try:
        minfo = info.find({'id': int(movie_id)}, {'_id': 0})
        for i in minfo:
            res.append(i)
        if len(res) != 1:
            raise Exception('`movie_id`索引错误！')
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        return None
    return res[0]


def getMovieList(movie_tag: str, page_count: int, page_cap: int):
    r"""
    获取默认情况下每页的电影列表，
    :param page_cap: 每页容量
    :param page_count: 页数（1,2,..,n）
    """
    res = []
    try:
        minfo = info.find({'genre': {'$regex': '.*{}.*'.format(movie_tag)}},
                          {'_id': 0, 'id': 1, 'name': 1, 'url': 1}).skip((page_count - 1) * page_cap).limit(page_cap)
        for i in minfo:
            res.append(i)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        return None
    return res


if __name__ == '__main__':
    # res = getMovieDetails(40)
    # print(res)
    # res2 = getMovieDetails(-1)
    # print(res2)
    res3 = getMovieList('Comedy', 1, 12)
    print(len(res3), res3)
