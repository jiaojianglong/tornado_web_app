#!usr/bin/env python
# -*- coding:utf-8 -*-

class Permission():
    method_code = {
        "GET": 1,
        "POST": 2,
        "PUT": 4,
        "DELETE": 8
    }

    @classmethod
    def vaild_permission(cls, method: str, code: int):
        method_code = cls.method_code.get(method.upper())
        if method_code & int(code) == method_code:
            return True
        return False

class Source():
    def __init__(self, uri: str, method: str):
        self.uri = uri
        self.method = method

