#!usr/bin/env python
# -*- coding:utf-8 -*-


from tornado.web import RequestHandler
from tornado.web import ObjectDict


class Page(ObjectDict):
    def __init__(self,
                 handler: RequestHandler,
                 page_arg: str = "page",
                 page_size_arg: str = "page_size"):
        self.handler = handler
        self.page_arg = page_arg
        self.page_size_arg = page_size_arg
        self.page_info = {
            "page": self.page,
            "page_size": self.page_size,
            "total": 0,
            "max_page": 0,
        }

    @property
    def page(self):
        return int(self.handler.get_argument(self.page_arg, "1"))

    @property
    def page_size(self):
        per_page = 20
        page_size = int(self.handler.get_argument(self.page_size_arg, "20"))
        if page_size < -1:
            page_size = per_page
        if page_size == -1:
            page_size = 1000
        if page_size > 1000:
            page_size = per_page
        return page_size

    @property
    def offset(self):
        return (self.page - 1) * self.page_size

    def set_page_info(self, total):
        self.page_info = {
            "page": self.page,
            "page_size": self.page_size,
            "total": total,
            "max_page": self._count_page(total, self.page_size)
        }

    def _count_page(self, total, page_size):
        if total % page_size > 0:
            return int(total / page_size) + 1
        else:
            return int(total / page_size)

    def query_by_page(self, query):
        total = query.count()
        objs = query.limit(self.page_size) \
            .offset(self.offset).all()
        self.set_page_info(total)
        return objs
