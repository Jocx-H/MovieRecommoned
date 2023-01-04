#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/2 12:09
@Author : Jocx-H
@File   : detailService.py
@Desc   :  PyCharm
'''

import json
import random
import traceback

from typing import Dict
from dao import infoDao


def __detail__(movie_id):
    try:
        movie_info = infoDao.getMovieDetails(movie_id)
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise e
    return movie_info


def getMovieDetail(movie_id) -> Dict:
    return {'result': __detail__(movie_id)}


if __name__ == '__main__':
    res = getMovieDetail(100)
    print(res)