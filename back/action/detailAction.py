#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/2 12:04
@Author : Jocx-H
@File   : detailAction.py
@Desc   :  前端调用电影详情页的api
'''


import traceback
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.encoders import jsonable_encoder

from action.msgCodeConf import Code400
from Service import detailService


# 构建api路由
router = APIRouter(
    prefix="/mdetail",
    tags=["Details"],
)


@router.post("/moviedetail", responses={400: {"model": Code400}})
def getMovieList(movie_id: int):
    r"""
    返回每一页的电影列表
    """
    try:
        movies = detailService.getMovieDetail(movie_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=Code400.detail)
    res = jsonable_encoder(movies)
    return res