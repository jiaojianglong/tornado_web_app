#!usr/bin/env python
# -*- coding:utf-8 -*-

import json

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.database import BaseModel


class Params(BaseModel):
    __tablename__ = "params"

    id = Column(Integer, primary_key=True, comment="配置id")
    name = Column(String(128), nullable=False)
    template_id = Column(Integer, ForeignKey("task_template.id"))
    params_str = Column(Text, nullable=False)
    template = relationship(
        'TaskTemplate',
        uselist=False,
        lazy="joined"
    )
    serialize_rules = ("actions", "-template")

    @classmethod
    def create_new(cls, params_info):
        params_obj = cls(
            name = params_info.get("name"),
            template_id = params_info.get("template_id")
        )
        params_obj.params = cls.get_params(params_info.get("actions"))
        return params_obj

    @classmethod
    def get_params(cls, actions):
        params = {}
        for index, action in enumerate(actions):
            params.update(
                {
                    str(action.get("id")) + "-" + str(index): action.get("params")
                }
            )
        return params

    def update(self, params_info):
        self.name = params_info.get("name")
        self.params = self.get_params(params_info.get("actions"))
        return self

    @property
    def params(self):
        return json.loads(self.params_str)

    @params.setter
    def params(self, value):
        self.params_str = json.dumps(value)

    @property
    def actions(self):
        actions = self.template.actions
        new_actions = []
        for index, action in enumerate(actions):
            action.params = self.params.get(str(action.id) + "-" + str(index))
            new_actions.append(action)
        return new_actions



