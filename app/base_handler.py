#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14
import json
import traceback
from typing import Any

from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from app.database import Session
from app.errors import CodeError, NotFoundError, HTTPError
from app.utils.page import Page
from concurrent.futures import ThreadPoolExecutor
from tornado.web import _ARG_DEFAULT, _ArgDefaultMarker, MissingArgumentError
from app.database import BaseModel


class BaseHandler(RequestHandler):
    _datamodel_: BaseModel
    executor = ThreadPoolExecutor(30)

    def initialize(self):
        self.db_session = None
        self.page = Page(self)

    # 通过 id 获取数据

    def item(self, id):
        if not self._datamodel_:
            raise CodeError("重写该方法或定义 __database__ 属性")

        item = self._datamodel_.query.get(id)
        if item is None:
            raise NotFoundError("{}:{}".format(self._datamodel_.__tablename__, id))
        self.set_response(data=self.to_dict(item))

    def prepare(self):

        if self.request.method == "GET":
            if (len(self.path_args) or len(self.path_kwargs)) and \
                    not len(self.request.query_arguments):
                self.get = self.item

        self.get = self.run_in_thread(self.get)
        self.post = self.run_in_thread(self.post)
        self.delete = self.run_in_thread(self.delete)
        self.put = self.run_in_thread(self.put)

    def auth(self):
        pass

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', 'http://127.0.0.1:8082')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE')
        self.set_header('Access-Control-Allow-Headers',
                        'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def on_connection_close(self):
        pass

    def to_dict(self, query_results):
        if isinstance(query_results, list):
            return [result.to_dict() for result in query_results]

        else:
            return query_results.to_dict()

    async def options(self, *args, **kwargs):
        self.finish()

    def success_response(self, data=None, message=""):
        response = {
            "status_code": 0,
            "message": message,
            "data": data,
            "pageinfo": self.page.page_info
        }
        self.write(response)

    def error_response(self, message="", data=None, status_code=404):
        self.set_status(status_code)
        response = {
            "status_code": status_code,
            "data": data,
            "message": message,
            "pageinfo": self.page.page_info
        }
        self.write(response)

    def set_response(self, data=None, message="", status_code=200):
        self.response_data = {
            "status_code": status_code,
            "data": data or {},
            "message": message,
        }

    def run_in_thread(self, fun):
        """让method运行在线程中"""

        async def inner(*args, **kwargs):
            await run_on_executor()(self.run_one_thread(fun))(self, *args, **kwargs)
            if hasattr(self, "response_data"):
                self.success_response(self.response_data.get("data"),
                                      self.response_data.get("message"))
                self.finish()
            return

        return inner

    def run_one_thread(self, fun):
        """在一个线程中运行，执行开始创建db_session，执行结束删除"""

        def inner(*args, **kwargs):
            if len(args):
                args = [arg for arg in args]
                args.pop(0)
            self.db_session = Session()
            self.auth()
            res = fun(*args, **kwargs)
            Session.remove()
            return res

        return inner

    def get_json_argument(self, name, default: Any = _ARG_DEFAULT):
        if not hasattr(self.request, "json_argument"):
            self.load_json()
        if name not in self.request.json_argument:
            if isinstance(default, _ArgDefaultMarker):
                raise MissingArgumentError(name)
            return default
        arg = self.request.json_argument[name]
        return arg

    def load_json(self):
        try:
            self.request.json_argument = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            raise HTTPError(400, msg, reason=msg)

    def write_error(self, status_code: int, **kwargs) -> None:
        """报错时返回"""
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header("Content-Type", "text/plain")
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            reason = kwargs.get("reason")
            if "exc_info" in kwargs:
                exception = kwargs["exc_info"][1]
                if isinstance(exception, HTTPError) and exception.log_message:
                    reason = exception.log_message
            self.error_response(reason, status_code=status_code)
            self.finish()

    def delete(self, id: str):
        obj = self._datamodel_.get_or_404(id)
        self.db_session.delete(obj)
        self.db_session.commit()
        return obj