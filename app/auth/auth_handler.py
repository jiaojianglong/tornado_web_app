#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

from app.auth.models.user import UserModel
from app.base_handler import BaseHandler
from app.errors import UnauthorizedError, ForbiddenError
from app.utils.jwt_cookie import JWT
from app import load_headlers


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

        return self.current_user


class PermissionHandler(AuthHandler):
    def auth(self):
        self.get_current_user()
        self.check_permission()

    def check_permission(self):
        if self.current_user.is_admin:
            return
        sources = [source for group in self.current_user.groups for source in group.sources]
        target_uris = self.get_target_uri()
        for source in sources:
            if source.get("uri") in target_uris:
                if self.request.method.upper() in source.get("methods"):
                    return
        raise ForbiddenError()

    def get_target_uri(self):
        handlers = load_headlers()
        target_uris = []
        for handler in handlers:
            if handler[1] == self.__class__:
                target_uris.append(handler[0])
        return target_uris
