# -*- coding:utf-8 -*-

import json

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.database import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, comment="任务id")
    status = Column(String(16), nullable=False, default="",
                         comment="任务状态")  # success failed executing unexecute waiting cancel

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        'UserModel',
        uselist=False,
        lazy='joined')

    template_id = Column(Integer, ForeignKey("task_template.id"))
    template = relationship(
        'TaskTemplate',
        uselist=False,
        lazy="joined"
    )

    @classmethod
    def create_new(cls, task_data, user):
        task = cls(
            template_id=task_data.get("id"),
            status="unexecute",
            user = user,
        )
        task.add_actions(task_data.get("actions", []))
        return task

    def add_actions(self, actions):
        actions_ins = []
        for index, action in enumerate(actions):
            action_ins = TaskAction(**{
                "action_code": action.get("action_code"),
            })
            action_ins.parameter = action.get("params", [])
            action_ins.sequence = index
            action_ins.name = action.get("name", "") or action.get("value")
            actions_ins.append(action_ins)

        self.actions = actions_ins


class TaskLog(BaseModel):
    __tablename__ = "task_log"

    id = Column(Integer, primary_key=True)

    log = Column(Text, nullable=False, default="")
    status = Column(String(27), nullable=False)

    action_id = Column(Integer, ForeignKey("task_action.id",
                                           ondelete="CASCADE"))
    task_id = Column(Integer, index=True)

    action = relationship(
        'TaskAction',
        uselist=False,
        lazy='select')


class TaskAction(BaseModel):
    __tablename__ = "task_action"

    id = Column(Integer, primary_key=True)

    name = Column(String(81), nullable=False, default="", comment="动作名称")
    action_code = Column(String(81), nullable=False, default="", comment="动作脚本")
    parameter_str = Column(String(1024), nullable=False, default='[]', comment="动作参数")
    sequence = Column(Integer, nullable=False, default=0, comment="执行顺序")

    task_id = Column(Integer, ForeignKey('task.id',ondelete="CASCADE"),index=True)

    task = relationship(
        'Task',
        backref=backref(
            'actions',
            cascade='all,delete-orphan',
            lazy='joined',
            order_by='TaskAction.sequence.asc()'
        ),
        uselist=False,
        lazy='joined')

    serialize_rules = ("-task", "parameter")

    @property
    def parameter(self):
        return json.loads(self.parameter_str)

    @parameter.setter
    def parameter(self, value):
        self.parameter_str = json.dumps(value)



