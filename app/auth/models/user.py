#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/14

import json

from sqlalchemy import Column, String, Text, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.errors import CodeError, NotFoundError
from app.utils.tools import md5
from app.database import BaseModel
from app.settings import Administrators

user_group = Table(
    "user_group",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), nullable=False, primary_key=True),
)


class UserModel(BaseModel):
    __tablename__ = "user"

    username = Column(String(length=30), nullable=False, unique=True, comment='用户名')
    password_code = Column(String(length=128), nullable=False, comment='密码')
    email = Column(String(length=64), comment="邮箱")

    serialize_rules = ("-password_code",)

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
        user = cls.search_one(username)
        return bool(user)

    @classmethod
    def search_one(cls, username: str):
        user = cls.query.filter(cls.username == username).first()
        return user

    @classmethod
    def get_user_by_name(cls, username: str):
        user = cls.query.filter(cls.username == username).first()
        if user is None:
            raise NotFoundError("{} username:{}".format(cls.__tablename__, username))
        return user

    @property
    def is_admin(self):
        if self.username in Administrators:
            return True
        return False


class GroupModel(BaseModel):
    __tablename__ = "group"

    groupname = Column(String(length=30), nullable=False, unique=True, comment='组名')
    source_ = Column(Text(), default="[]", nullable=False, comment="资源")

    users = relationship(
        'UserModel',
        secondary=user_group,
        backref=backref('groups', lazy='joined'),
        lazy='dynamic')

    serialize_rules = ("-users.groups", "-source_", "sources")
    @property
    def sources(self):
        return json.loads(self.source_)

    @sources.setter
    def sources(self, val: list):
        self.source_ = json.dumps(val)
