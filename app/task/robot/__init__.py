#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
参数定义格式
[
{
"type": "int" #["str", "int", "list", "bool", "file"]
"describe": "描述",
"name": "参数名",
"nullable": False [True, False],
"default":12,
"options":[12, 13, 24, 36],
}
]
"""


class BaseRobot():

    def __init__(self, manage, logger):
        self.logger = logger
        self.manage = manage


class WebRobot(BaseRobot):
    LocalDriver=False


