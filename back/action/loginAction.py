#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/4 20:02
@Author : Jocx-H
@File   : loginAction.py
@Desc   :  PyCharm
'''


import traceback
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.encoders import jsonable_encoder

from action.msgCodeConf import Code400
from Service import loginService


# 构建api路由
router = APIRouter(
    prefix="/login",
    tags=["Login"],
)


@router.post("/login", responses={400: {"model": Code400}})
def login(usr: str):
    r"""
    登录服务
    """
    try:
        res = loginService.isLogin(usr)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=Code400.detail)
    res = jsonable_encoder(res)
    return res