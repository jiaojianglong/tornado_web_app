#!usr/bin/env python
# -*- coding:utf-8 -*-
# author: jiaojianglong
# @time: 2020/07/14

from sqlalchemy import Column, String
from app.database import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    username = Column(String(length=30), comment='用户名')
    password_code = Column(String(length=128), comment='密码')
    email = Column(String(length=64), comment="邮箱")

