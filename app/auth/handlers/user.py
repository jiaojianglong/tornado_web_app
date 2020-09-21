#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/15

from app.base_handler import BaseHandler
from app.errors import AlreadyExistError
from app.errors import BadRequestError, ForbiddenError
from app.auth.auth_handler import AuthHandler
from app.auth.models.user import UserModel
from app.utils.jwt_cookie import JWT


class LoginHandler(BaseHandler):

    def post(self):
        username = self.get_json_argument("username")
        password = self.get_json_argument("password")

        user = UserModel.search_one(username)
        if not user:
            raise BadRequestError("username wrong")
        if not user.valid_password(password):
            raise BadRequestError("password wrong")

        jwt_cookie = JWT.get_cookie({"username": user.username})
        self.set_cookie("jwt_cookie", jwt_cookie)
        self.set_response(data=self.to_dict(user))


class LogoutHandler(AuthHandler):
    def post(self):
        self.clear_cookie("jwt_cookie")
        self.set_response(message="success")


class UserHandler(AuthHandler):
    _datamodel_ = UserModel

    def item(self, id):
        self.set_response(data=self.to_dict(self.current_user))

    def get(self):
        username = self.get_argument("username")
        users = self._datamodel_.query.filter(self._datamodel_.username == username).all()
        self.set_response(data=self.to_dict(users))

    def post(self):
        username = self.get_json_argument("username")
        password = self.get_json_argument("password")
        email = self.get_json_argument("email")

        if self._datamodel_.is_exist(username):
            raise AlreadyExistError("username: {}".format(username))
        user = self._datamodel_(username=username, password=password, email=email)
        self.db_session.add(user)
        self.db_session.commit()
        self.set_response(data=self.to_dict(user))

    def put(self, id: str):
        if self.current_user.id != int(id):
            raise ForbiddenError()
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("new_password")
        if not self.current_user.valid_password(old_password):
            raise BadRequestError("old_password wrong")
        self.current_user.password = new_password
        self.db_session.add(self.current_user)
        self.db_session.commit()
        self.set_response(data=self.to_dict(self.current_user))

    def delete(self, id: str):
        if self.current_user.id != int(id):
            raise ForbiddenError()
        super(UserHandler, self).delete(id)

