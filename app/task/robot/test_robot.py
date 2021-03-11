#!usr/bin/env python
# -*- coding:utf-8 -*-
from app.task.robot import BaseRobot


class TestRobot(BaseRobot):
    """
describe: 测试动作
params:[{
"type": "int",
"describe": "年龄年龄",
"name": "age",
"show_name": "年龄",
"required": false,
"default": 12,
"options": [{"label":12, "value":12}, {"label":15, "value":15},{"label":18, "value" :18}]
},{
"type": "list",
"describe": "年龄年龄",
"name": "names",
"show_name": "用户",
"required": true,
"default": [15],
"options": [{"label":12, "value":12}, {"label":15, "value":15},{"label":18, "value" :18}]
},{
"type": "bool",
"describe": "是否及格",
"name": "is_grade",
"show_name": "是否及格",
"required": true,
"default": true
}]
    """
    def __init__(self, logger, manage, **params):
        super().__init__(logger, manage)
        self.names = params.get("names")
        self.age = params.get("age")
        self.is_grade = params.get("is_grade")

    def run(self):
        self.logger.info("执行脚本-{}-{}-{}".format(self.names, self.age, self.is_grade))
