#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/13
from .handlers.user import LoginHandler, UserHandler, LogoutHandler

base_url = "/api/v1/user"
handlers = [
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/", UserHandler),
    (r"/([0-9]+)", UserHandler)
]

__all__ = [
    "handlers", "base_url"
]
