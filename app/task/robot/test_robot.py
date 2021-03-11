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

    def __init__(self, age, names, is_grade):
        self.age = age
        self.names = names
        self.is_grade = is_grade

    def run(self):
        print("执行脚本", self.names, self.age, self.is_grade)
