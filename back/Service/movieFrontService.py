#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/2 12:09
@Author : Jocx-H
@File   : movieFrontService.py
@Desc   :  PyCharm
'''


import json
import random
import traceback

from dao import infoDao


PAGE_CAP = 12  # 每一页电影的数量
movie_tag = {
    1: 'Action', 2: 'Adventure', 3: 'Animation', 4: 'Children', 5: 'Comedy', 6: 'Fantasy',
    7: 'IMAX', 8: 'Romance', 9: 'Sci-Fi', 10: 'Western', 11: 'Crime', 12: 'Mystery',
    13: 'Drama', 14: 'Thriller', 15: 'War', 16: 'Horror', 17: 'Film-Noir', 18: 'Documentary',
    19: 'Musical', 20: 'Others'
}


def __movies__(t, pc):
    mid = []
    urls = []
    names = []
    try:
        movie_list = infoDao.getMovieList(movie_tag[t], pc, PAGE_CAP)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise e
    for m in movie_list:
        mid.append(m['id'])
        names.append(m['name'])
        urls.append(m['url'])
    return {'id': mid, 'name': names, 'url': urls}


def getMovieList(tag, page_count):
    return {'result': __movies__(tag, page_count)}


if __name__ == '__main__':
    print(getMovieList(3, 4))