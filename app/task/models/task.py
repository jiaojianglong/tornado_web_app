# -*- coding:utf-8 -*-

import json
import datetime

from sqlalchemy import Column, String, Text, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from app.database import BaseModel


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, comment="任务id")
    status = Column(String(16), nullable=False, default="",
                         comment="任务状态")  # success failed executing unexecute waiting cancel
    params_id = Column(Integer, ForeignKey("params.id"))
    params = relationship(
        "Params",
        uselist=False,
        lazy='joined')

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
            params = task_data,
            template_id=task_data.template_id,
            status="unexecute",
            user = user,
        )
        task.add_actions(task_data.actions)
        return task

    def add_actions(self, actions):
        actions_ins = []
        for index, action in enumerate(actions):
            action_ins = TaskAction(**{
                "action_code": action.action_code,
            })
            action_ins.parameter = action.params
            action_ins.sequence = index
            action_ins.name = action.name
            actions_ins.append(action_ins)

        self.actions = actions_ins


class TaskLog(BaseModel):
    __tablename__ = "task_log"

    id = Column(Integer, primary_key=True)

    log_str = Column(Text, nullable=False, default="")
    status = Column(String(27), nullable=False)

    action_id = Column(Integer, ForeignKey("task_action.id",
                                           ondelete="CASCADE"))

    action = relationship(
        'TaskAction',
        backref=backref(
            'action_log',
            cascade='all,delete-orphan',
            lazy='joined',
            uselist=False
        ),
        uselist=False,
        lazy='joined'
        )

    @property
    def logger(self):
        if self.log_str:
            return json.loads(self.log_str)
        return []

    @logger.setter
    def logger(self, value):
        self.log_str = json.dumps(value)

    def info(self, message):
        return self.add_log("info", message)

    def warning(self, message):
        return self.add_log("warning", message)

    def error(self, message):
        return self.add_log("error", message)

    def add_log(self, status, message):
        logger = self.logger
        logger.append({
            "status": status,
            "message": message,
            "time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.logger = logger
        return self

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



