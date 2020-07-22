#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/13
from .handlers.user import LoginHandler, UserHandler

base_url = "/api/v1/user"
handlers = [
    (r"/login", LoginHandler),
    (r"/", UserHandler),
    (r"/([a-zA-Z0-9]+)", UserHandler)
]

__all__ = [
    "handlers", "base_url"
]
