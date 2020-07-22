#!usr/bin/env python
# -*- coding:utf-8 _*-
import os

ROOT = os.path.dirname(__file__)

APPS = "auth"

DB_INFO = {
    "DB_USER": "root",
    "DB_PWD": "123456",
    "DB_HOST": "192.168.0.100",
    "DB_PORT": "3306",
    "DB_NAME": "tornado_web"
}

JWT_SECRET = "as34gf3d8ge5r6he0r7"