#! /usr/bin/python3
# -*- codeing = utf-8 -*-
'''
@Time   : 2023/1/2 14:17
@Author : Jocx-H
@File   : msgCodeConf.py
@Desc   :  配置各种状态码的返回信息
'''


from pydantic import BaseModel


class Code400(BaseModel):
    detail: str = "客户端运行错误，请检查输入内容或联系管理员！"


class Code403(BaseModel):
    detail: str = "客户端请求权限不足"