#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/15

import jwt

from app.errors import AlreadyExistError
from app.errors import BadRequestError, ForbiddenError
from app.settings import JWT_SECRET
from auth.base_handler import BaseHandler
from ..models.user import UserModel


class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        user = UserModel.search_one(username)
        if not user:
            raise BadRequestError("username wrong")
        if not user.valid_password(password):
            raise BadRequestError("password wrong")
        headers = {"alg": "HS256", "typ": "JWT"}

        payload = {
            "username": user.username,
        }
        jwt_cookie = jwt.encode(payload=payload,
                                key=JWT_SECRET,
                                algorithm='HS256',
                                headers=headers).decode('utf-8')
        self.set_cookie("jwt_cookie", jwt_cookie)
        self.write(user.to_dict())


class LogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie("jwt_cookie")
        self.write("success")


class UserHandler(BaseHandler):
    _datamodel_ = UserModel

    def get(self):
        username = self.get_argument("username")
        users = self._datamodel_.query.filter(self._datamodel_.username == username).all()
        self.write(self.to_json(users))

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        email = self.get_argument("email")

        if self._datamodel_.is_exist(username):
            raise AlreadyExistError("username: {}".format(username))
        user = self._datamodel_(username=username, password=password, email=email)
        self.db_session.add(user)
        self.db_session.commit()
        self.write(self.to_json(user))

    def put(self, id: str):
        if self.user.id != int(id):
            raise ForbiddenError()
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("new_password")
        if not self.user.valid_password(old_password):
            raise BadRequestError("old_password wrong")
        self.user.password = new_password
        self.db_session.add(self.user)
        self.db_session.commit()
        self.write(self.to_json(self.user))

    def delete(self, id: str):
        if self.user.id != int(id):
            raise ForbiddenError()
        super(UserHandler, self).delete(id)
