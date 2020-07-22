#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14
import json

from tornado.web import RequestHandler
from app.database import Session
from app.errors import CodeError, NotFoundError


class UnauthorizedHandler(RequestHandler):
    _datamodel_ = ""

    def _initialize(self):
        pass

    # 通过 id 获取数据

    def item(self, id):
        if not self._datamodel_:
            raise CodeError("重写该方法或定义 __database__ 属性")

        item = self._datamodel_.query.get(id)
        if item is None:
            raise NotFoundError("{}:{}".format(self._datamodel_.__tablename__, id))
        self.write(item.to_dict())

    def prepare(self):
        self.db_session = Session()

        # 将 GET id 重定向到 item()
        if self.request.method == "GET":
            if (len(self.path_args) or len(self.path_kwargs)) and \
                    not len(self.request.query_arguments):
                self.get = self.item

    def on_finish(self):
        if hasattr(self, "db_session"):
            self.db_session.close()

    def on_connection_close(self):
        pass

    def to_json(self, query_results):
        if isinstance(query_results, list):
            return json.dumps([result.to_dict() for result in query_results])

        else:
            return query_results.to_dict()


class BaseHandler(UnauthorizedHandler):
    def _initialize(self):
        pass

    def on_connection_close(self):
        pass
