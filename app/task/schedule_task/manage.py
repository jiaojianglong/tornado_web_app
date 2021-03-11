#!usr/bin/env python
# -*- coding:utf-8 -*-
from settings import ACTION_CONFIG
import importlib
from app.database import Session
from app.task.models.task import TaskLog
from app.task.schedule_task.action_log import ActionLog


class Manage():

    def __init__(self, task):
        self.task = task
        self.db_session = Session()

    def run(self):
        self.set_executing()
        for action in self.task.actions:
            if not self.run_action(action):
                break
        else:
            self.set_success()

    def run_action(self, action):
        self.logger = ActionLog(self.db_session, action)
        self.logger.executing_status("开始执行")
        try:
            action_config = ACTION_CONFIG.get(action.action_code)
            action_module = importlib.import_module(action_config.get("package"))
            params = {params.get("name"): params.get("value") for params in action.parameter}
            self.logger.info("参数：{}".format(params))
            action_obj = getattr(action_module, action_config.get("action_class"))(self,
                                                                                   self.logger,
                                                                                   **params)
            action_obj.run()
        except Exception as e:
            self.logger.failed_status(str(e))
            self.set_failed()
            return False
        self.logger.success_status("执行成功")
        return True

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
