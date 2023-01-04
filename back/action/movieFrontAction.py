#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/2 12:04
@Author : Jocx-H
@File   : movieFrontAction.py
@Desc   :  前端首页调用电影的api
'''


import traceback
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.encoders import jsonable_encoder

from action.msgCodeConf import Code400
from Service import movieFrontService


# 构建api路由
router = APIRouter(
    prefix="/mfront",
    tags=["MovieFront"],
)


@router.post("/movielist", responses={400: {"model": Code400}})
def getMovieList(tag: int, page_count: int):
    r"""
    返回每个分类的每一页的电影列表
    """
    try:
        movies = movieFrontService.getMovieList(tag, page_count)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=Code400.detail)
    return jsonable_encoder(movies)