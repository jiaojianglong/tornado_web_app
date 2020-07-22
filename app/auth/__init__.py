#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/13
from .handlers.user import LoginHandler, UserHandler

handlers = [
    (r"/user/login", LoginHandler),
    (r"/user", UserHandler),
    (r"/user/([a-zA-Z0-9]+)", UserHandler)
]

__all__ = [
    "handlers"
]
