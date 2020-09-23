#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/13
from app.auth.handlers.user import LoginHandler, UserHandler, LogoutHandler
from app.auth.handlers.group import GroupHandler
from app.auth.handlers.source import SourceHandler

base_url = "/api/v1/auth"
handlers = [
    (r"/user_login", LoginHandler),
    (r"/user_logout", LogoutHandler),
    (r"/users", UserHandler),
    (r"/users/([0-9a-z]+)", UserHandler),
    (r"/groups", GroupHandler),
    (r"/groups/([0-9a-z]+)", GroupHandler),
    (r"/sources", SourceHandler)
]

__all__ = [
    "handlers", "base_url"
]
