#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/13
from app.auth.handlers.user import LoginHandler, UserHandler, LogoutHandler

base_url = "/api/v1/auth"
handlers = [
    (r"/user_login", LoginHandler),
    (r"/user_logout", LogoutHandler),
    (r"/users", UserHandler),
    (r"/users/([0-9a-z]+)", UserHandler)
]

__all__ = [
    "handlers", "base_url"
]
