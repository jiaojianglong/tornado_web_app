#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.task.models.task import TaskLog

class ActionLog:
    def __init__(self, db_session, action):
        self.db_session = db_session
        self.action = self.init_action_log(action)
        self.action_log_obj = self.action.action_log

    def init_action_log(self, action):
        if not action.action_log:
            action.action_log = TaskLog()
            self.commit(action)
        return action


    def info(self, message):
        obj = self.action_log_obj.add_log("info", message)
        self.commit(obj)

    def warning(self, message):
        obj = self.action_log_obj.add_log("warning", message)
        self.commit(obj)

    def error(self, message):
        obj = self.action_log_obj.add_log("error", message)
        self.commit(obj)

    def failed_status(self, message):
        obj = self.action_log_obj.add_log("error", message)
        obj.status = "failed"
        self.commit(obj)

    def executing_status(self, message):
        obj = self.action_log_obj.add_log("state", message)
        obj.status = "executing"
        self.commit(obj)

    def success_status(self, message):
        obj = self.action_log_obj.add_log("state", message)
        obj.status = "success"
        self.commit(obj)

    def commit(self, obj):
        self.db_session.add(obj)
        self.db_session.commit()
