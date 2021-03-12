#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.auth.auth_handler import PermissionHandler
from app.task.models.task import TaskLog, Task


class TaskLogHandler(PermissionHandler):
    _datamodel_ = TaskLog

    def get(self):
        task_id = self.get_argument("task_id")
        task = Task.get_or_404(task_id)
        actions = task.actions
        self.set_response(data=self.to_dict(actions))
