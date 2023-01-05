#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/5 13:24
@Author : Jocx-H
@File   : movie_recom_action.py
@Desc   :  PyCharm
'''


import traceback
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.encoders import jsonable_encoder

from action.msgCodeConf import Code400
from service import movie_recom_service


# 构建api路由
router = APIRouter(
    prefix="/agri",
    tags=["AgriMovie"],
)


@router.get("/recommovie", responses={400: {"model": Code400}})
def getRecomMovieList(usr: str, curr_type: str):
    r"""
    返回初始的热门电影
    """
    try:
        movies = movie_recom_service.getRecomMovieList([usr, curr_type])
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=Code400.detail)
    return jsonable_encoder(movies)