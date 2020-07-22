#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

from tornado.web import HTTPError


class UnauthorizedError(HTTPError):
    def __init__(self) -> None:
        super(UnauthorizedError, self).__init__(
            401, "Unauthorized", reason="Unauthorized"
        )
        self.arg_name = "Unauthorized"


class ForbiddenError(HTTPError):
    def __init__(self) -> None:
        super(ForbiddenError, self).__init__(
            403, "Forbidden", reason="Forbidden"
        )
        self.arg_name = "Forbidden"


class BadRequestError(HTTPError):
    def __init__(self, arg_name: str) -> None:
        super(BadRequestError, self).__init__(
            400, arg_name, reason=arg_name
        )
        self.arg_name = arg_name


class CodeError(HTTPError):
    def __init__(self, arg_name: str) -> None:
        super(CodeError, self).__init__(
            500, arg_name, reason=arg_name
        )
        self.arg_name = arg_name


class NotFoundError(HTTPError):
    def __init__(self, arg_name: str) -> None:
        reason = "not found {}".format(arg_name)
        super(NotFoundError, self).__init__(
            400, reason, reason=reason
        )
        self.arg_name = reason


class AlreadyExistError(HTTPError):
    def __init__(self, arg_name: str) -> None:
        reason = "already exist: {}".format(arg_name)
        super(AlreadyExistError, self).__init__(
            400, reason, reason=reason
        )
        self.arg_name = reason
