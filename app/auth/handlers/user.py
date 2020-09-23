#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/15

from app.base_handler import BaseHandler
from app.errors import AlreadyExistError
from app.errors import BadRequestError, ForbiddenError
from app.auth.auth_handler import AuthHandler, PermissionHandler
from app.auth.models.user import UserModel, GroupModel
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


class UserHandler(PermissionHandler):
    _datamodel_ = UserModel

    def item(self, id):
        self.set_response(data=self.to_dict(self.current_user))

    def get(self):
        username = self.get_argument("username", "")
        query = self._datamodel_.query.filter(
            self._datamodel_.username.like("%{}%".format(username)),
        )
        users = self.page.query_by_page(query)
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
        if self.current_user.id != int(id) and not self.current_user.is_admin:
            raise ForbiddenError()

        username = self.get_json_argument("username")
        email = self.get_json_argument("email")
        groupnames = self.get_json_argument("groups", [])
        user = self._datamodel_.query.get(id)
        if groupnames:
            groups = GroupModel.query.filter(
                GroupModel.groupname.in_(groupnames)
            ).all()
            user.groups = groups
        user.username = username
        user.email = email
        self.db_session.add(user)
        self.db_session.commit()
        self.set_response(data=self.to_dict(user))

    def delete(self, id: str):
        if self.current_user.id != int(id) and not self.current_user.is_admin:
            raise ForbiddenError()
        user = super(UserHandler, self).delete(id)
        self.set_response(message="success")

