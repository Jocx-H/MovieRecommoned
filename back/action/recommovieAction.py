#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/4 16:59
@Author : Jocx-H
@File   : recommovieAction.py
@Desc   :  PyCharm
'''


import traceback
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.encoders import jsonable_encoder

from action.msgCodeConf import Code400
from Service import recommovieService


# 构建api路由
router = APIRouter(
    prefix="/recom",
    tags=["RcomMovie"],
)


@router.get("/hotmovie", responses={400: {"model": Code400}})
def getHotMovieList():
    r"""
    返回初始的热门电影
    """
    try:
        movies = recommovieService.getHotMovieList()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=Code400.detail)
    return jsonable_encoder(movies)