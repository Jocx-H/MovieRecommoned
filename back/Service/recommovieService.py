#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/4 17:02
@Author : Jocx-H
@File   : recommovieService.py
@Desc   :  PyCharm
'''


import json
import random
import traceback

from dao import hotDao


PAGE_CAP = 12  # 每一页电影的数量


def __movies__():
    mid = []
    urls = []
    names = []
    try:
        movie_list = hotDao.getHotMovieList()
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise e
    for m in movie_list:
        mid.append(m['id'])
        names.append(m['name'])
        urls.append(m['url'])
    return {'id': mid, 'name': names, 'url': urls}


def getHotMovieList():
    return {'result': __movies__()}


if __name__ == '__main__':
    print(getHotMovieList())