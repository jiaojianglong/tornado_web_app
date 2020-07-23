#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

import jwt
from tornado.web import RequestHandler

from app.errors import CodeError, UnauthorizedError
from app.settings import JWT_SECRET
from auth.database import Session
from auth.models.user import UserModel


class BaseHandler(RequestHandler):
    _datamodel_ = ""

    def _initialize(self):
        pass

    # 通过 id 获取数据

    def item(self, id: str):
        if not self._datamodel_:
            raise CodeError("重写该方法或定义 __database__ 属性")

        item = self._datamodel_.get_or_404(id)
        self.write(item.to_dict())

    def delete(self, id: str):
        if not self._datamodel_:
            raise CodeError("重写该方法或定义 __database__ 属性")

        item = self._datamodel_.remove(id)
        self.db_session.add(item)
        self.db_session.commit()
        self.write(item.to_dict())

    def prepare(self):
        self.db_session = Session()

        # 将 GET id 重定向到 item()
        if self.request.method == "GET":
            if (len(self.path_args) or len(self.path_kwargs)) and \
                    not len(self.request.query_arguments):
                self.get = self.item

        if self.is_skip_auth(self.request.method, self.request.uri):
            return

        jwt_cookie = self.get_cookie("jwt_cookie")
        if not jwt_cookie:
            raise UnauthorizedError()
        info = jwt.decode(jwt_cookie, JWT_SECRET, True, algorithm='HS256')

        user = UserModel.get_user_by_name(info.get("username"))
        self.user = user

    def on_finish(self):
        if hasattr(self, "db_session"):
            self.db_session.close()

    def on_connection_close(self):
        pass

    def to_json(self, query_results):
        if isinstance(query_results, list):
            return [result.to_dict() for result in query_results]

        else:
            return query_results.to_dict()

    def is_skip_auth(self, method: str, uri: str):
        skip_path = [
            ()
        ]

# from app.auth.models.user import UserModel