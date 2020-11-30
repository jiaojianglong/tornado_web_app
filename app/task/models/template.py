#!usr/bin/env python
# -*- coding:utf-8 -*-
import json

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.database import BaseModel
from app.task.models.action import Action


class TaskTemplate(BaseModel):
    __tablename__ = 'task_template'

    id = Column(Integer, primary_key=True)

    name = Column(String(27), nullable=False, comment="任务模板名称")
    description = Column(String(1024), nullable=False, default="", comment="模板描述")

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        'UserModel',
        uselist=False,
        lazy='joined')

    serialize_rules = ("-actions_db.template", "-actions_db.action", "actions")

    @classmethod
    def create_new(cls, template_data):
        template = cls(
            name=template_data.get("name"),
            description=template_data.get("description", ""),
            actions=template_data.get("actions", [])
        )
        return template

    @property
    def actions(self):
        actions = [Action.query.get(action.action_id) for action in self.actions_db]
        return actions

    @actions.setter
    def actions(self, actions):
        actions_db_ins = []
        for index, action in enumerate(actions):
            action_db_ins = TemplateAction(
                sequence=index,
                action_id=action.get("id"),
            )
            actions_db_ins.append(action_db_ins)
        self.actions_db = actions_db_ins

class TemplateAction(BaseModel):
    """template action 多对多"""
    __tablename__ = "template_action"

    id = Column(Integer, primary_key=True)

    sequence = Column(Integer, nullable=False, default=0, comment="执行顺序")

    template_id = Column(Integer, ForeignKey('task_template.id',
                                             ondelete="CASCADE"),
                         nullable=False, index=True)

    action_id = Column(Integer,
                       ForeignKey('action.id', ondelete="RESTRICT"),
                       nullable=False)

    template = relationship(
        'TaskTemplate',
        backref=backref(
            'actions_db',
            cascade='all,delete-orphan',
            lazy='joined',
            order_by='TemplateAction.sequence.asc()'
        ),
        uselist=False,
        lazy='joined')

    action = relationship(
        'Action',
        backref=backref(
            'actions_db',
            lazy='joined',
        ),
        uselist=False,
        lazy='joined')


