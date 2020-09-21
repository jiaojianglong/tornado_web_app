#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/14

import json

from sqlalchemy import Column, String, Text, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.errors import CodeError, NotFoundError
from app.utils.tools import md5
from app.database import BaseModel

user_group = Table(
    "user_group",
    BaseModel.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), nullable=False, primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), nullable=False, primary_key=True),
    keep_existing=True
)


class UserModel(BaseModel):
    __tablename__ = "user"

    username = Column(String(length=30), nullable=False, unique=True, comment='用户名')
    password_code = Column(String(length=128), nullable=False, comment='密码')
    email = Column(String(length=64), comment="邮箱")
    groups = relationship("GroupModel", secondary=user_group)

    serialize_rules = ("username", "email", "groups")

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
        user = cls.query.filter(cls.username == username, cls.is_enable == 1).first()
        return user

    @classmethod
    def get_user_by_name(cls, username: str):
        user = cls.query.filter(cls.username == username).first()
        if user is None:
            raise NotFoundError("{} username:{}".format(cls.__tablename__, username))
        if user.is_enable is False:
            raise NotFoundError("已删除 {} username:{}".format(cls.__tablename__, username))
        return user


class GroupModel(BaseModel):
    __tablename__ = "group"

    groupname = Column(String(length=30), nullable=False, unique=True, comment='组名')
    source_ = Column(Text(), default="[]", nullable=False, comment="资源")

    users = relationship("UserModel", secondary=user_group)

    serialize_rules = ("groupname", "sources", "users")
    @property
    def sources(self):
        return json.loads(self.source_)

    @sources.setter
    def sources(self, val: list):
        self.source_ = json.dumps(val)
