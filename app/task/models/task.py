# -*- coding:utf-8 -*-

import json

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.database import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, comment="任务id")

    description = Column(String(1024), nullable=False, default="", comment="任务描述")
    parameter_str = Column(Text, nullable=False, default="[]", comment="执行参数")
    task_code = Column(String(80), nullable=False, default="", comment="执行脚本")
    status = Column(String(16), nullable=False, default="",
                         comment="任务状态")  # success failed executing unexecute waiting cancel

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(
        'UserModel',
        uselist=False,
        lazy='joined')

    @property
    def parameter(self):
        return json.loads(self.parameter_str)

    @parameter.setter
    def parameter(self, value):
        self.parameter_str = json.dumps(value)

    @classmethod
    def create_new(cls, task_data, user):
        task = cls(
            description=task_data.get("description", ""),
            task_code=task_data.get("task_code"),
            status="unexecute",
            parameter=task_data.get("parameter", []),
            user = user,
        )
        task.add_actions(task_data.get("actions", []))
        task.save()
        return task

    def add_actions(self, actions):
        actions_ins = []
        for index, action in enumerate(actions):
            action_ins = TaskAction(**{
                "action_code": action.get("action_code"),
            })
            action_ins.task = self
            action_ins.parameter = action.get("parameter", [])
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
            order_by='Action.sequence.asc()'
        ),
        uselist=False,
        lazy='joined')

    @property
    def parameter(self):
        return json.loads(self.parameter_str)

    @parameter.setter
    def parameter(self, value):
        self.parameter_str = json.dumps(value)



