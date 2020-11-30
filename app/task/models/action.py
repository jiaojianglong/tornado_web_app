#!usr/bin/env python
# -*- coding:utf-8 -*-

import json

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import BaseModel


class Action(BaseModel):
    """动作"""
    __tablename__ = "action"

    id = Column(Integer, primary_key=True)

    name = Column(String(81), nullable=False, comment="动作名称")
    action_code = Column(String(81), nullable=False, comment="动作脚本")
    description = Column(String(81), nullable=False, comment="动作描述")
    parameter_str = Column(String(1024), nullable=False, default='[]',comment="动作参数")

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        'UserModel',
        uselist=False,
        lazy='joined')

    serialize_rules = ("params", "-actions_db.template", "-actions_db.action")
    @property
    def params(self):
        return json.loads(self.parameter_str)

    @params.setter
    def params(self, value):
        self.parameter_str = json.dumps(value)

    @classmethod
    def create_new(cls, data, user):
        ins = cls(
            name=data.get("name"),
            action_code=data.get("action_code"),
            parameter=data.get("parameter"),
        )
        ins.user = user
        ins.save()
        return ins

    def add_parameter(self, parameter):
        for par in parameter:
            if not par.get("value") and par.get("value") != 0:
                par["level"] = "template"
            else:
                par["level"] = "action"

        return parameter

    def update(self, data):
        self.name = data.get("name")
        self.parameter = self.add_parameter(data.get("parameter", []))
        self.save()
