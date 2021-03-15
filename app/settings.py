#!usr/bin/env python
# -*- coding:utf-8 _*-
import os

ROOT = os.path.dirname(__file__)

APPS = "auth,task"

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI",
                                         "mysql+pymysql://root:123456@127.0.0.1:3306/tornado_web")

JWT_SECRET = "as34gf3d8ge5r6he0r7"

Administrators = ["jiao"]

ACTION_CONFIG = {
    "test_action": {
        "package": "app.task.robot.test_robot",
        "action_class": "TestRobot"
    }
}

WXBot = {
    "host":"127.0.0.1",
    "accept_port": 8666,
    "send_port": 8777
}