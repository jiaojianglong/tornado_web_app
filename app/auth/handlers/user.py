#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/15

from app.base_handler import UnauthorizedHandler, BaseHandler
from ..models.user import UserModel


class LoginHandler(UnauthorizedHandler):
    def get(self):
        user = UserModel.query.filter(UserModel.username == "jiao").first()
        print(user)
        # user = UserModel(username="jiao", password="123")
        # self.db_session.add(user)
        # self.db_session.commit()
        self.write(r"success")


class UnloginHandler(BaseHandler):
    def post(self):
        pass


class UserHandler(BaseHandler):
    _datamodel_ = UserModel

    def get(self):
        username = self.get_argument("username")
        users = self._datamodel_.query.filter(self._datamodel_.username == username).all()
        self.write(self.to_json(users))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
