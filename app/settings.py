#!usr/bin/env python
# -*- coding:utf-8 _*-
import os

ROOT = os.path.dirname(__file__)

APPS = "auth"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/tornado_web"

JWT_SECRET = "as34gf3d8ge5r6he0r7"
