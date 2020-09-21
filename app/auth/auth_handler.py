#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

from app.auth.models.user import UserModel
from app.base_handler import BaseHandler
from app.errors import UnauthorizedError
from app.utils.jwt_cookie import JWT


class AuthHandler(BaseHandler):

    def auth(self):
        self.get_current_user()

    def get_current_user(self):
        cookie = self.get_cookie("jwt_cookie")
        payload = JWT.get_payload(cookie)
        if not payload:
            raise UnauthorizedError()

        username = payload.get("username")
        self.current_user = UserModel.get_user_by_name(username)
        print(self.current_user)
        return self.current_user

    def get_login_url(self) -> str:
        """Override to customize the login URL based on the request.

        By default, we use the ``login_url`` application setting.
        """
        self.require_setting("login_url", "@tornado.web.authenticated")
        return self.application.settings["login_url"]