#!usr/bin/env python
# -*- coding:utf-8 -*-
from settings import ACTION_CONFIG
import importlib
from app.database import Session
from app.task.models.task import TaskLog


class Manage():

    def __init__(self, task):
        self.task = task
        self.db_session = Session()

    def run(self):
        self.set_executing()
        for action in self.task.actions:
            action.action_log = TaskLog(status="executing")
            try:
                action_config = ACTION_CONFIG.get(action.action_code)
                action_module = importlib.import_module(action_config.get("package"))
                params = {params.get("name"): params.get("value") for params in action.parameter}
                print(params)
                action_obj = getattr(action_module, action_config.get("action_class"))(**params)
                action_obj.run()
            except Exception as e:
                action.action_log.error(str(e))
                self.set_failed()
            self.logger(action.action_log.info, "执行成功")

    def logger(self, func, message):
        obj = func(message)
        self.db_session.add(obj)
        self.db_session.commit()


    def set_failed(self):
        self.set_status("failed")

    def set_executing(self):
        self.set_status("executing")

    def set_cancel(self):
        self.set_status("cancel")

    def set_waiting(self):
        self.set_status("waiting")

    def set_success(self):
        self.set_status("success")

    def set_status(self, status):
        self.task.status = status
        self.db_session.add(self.task)
        self.db_session.commit()
