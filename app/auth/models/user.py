#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/14

from sqlalchemy import Column, String
from app.database import BaseModel
from app.utils.tools import md5
from app.errors import CodeError


class UserModel(BaseModel):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    username = Column(String(length=30), comment='用户名')
    password_code = Column(String(length=128), comment='密码')
    email = Column(String(length=64), comment="邮箱")

    serialize_rules = ("username", "email")

    @property
    def password(self):
        raise CodeError("不允许获取密码")

    @password.setter
    def password(self, val: str):
        self.password_code = md5(val)

    def valid_password(self, val: str):
        return md5(val) == self.password_code

    @classmethod
    def is_exist(cls, username: str):
        user = cls.search(username)
        return bool(user)

    @classmethod
    def search(cls, username: str):
        user = cls.query.filter(cls.username == username, cls.is_enable is True).first()
        return user
