#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.task.handlers.action import ActionHandler, ActionCodeHandler
from app.task.handlers.template import TemplateHandler
from app.task.handlers.task import TaskHandler
from app.task.handlers.params import ParamsHandler
from app.task.handlers.task_log import TaskLogHandler
from app.task.schedule_task import run

base_url = "/api/v1/task"
handlers = [
    (r"/action", ActionHandler),
    (r"/action/([0-9a-z]+)", ActionHandler),
    (r"/action_code", ActionCodeHandler),
    (r"/template", TemplateHandler),
    (r"/template/([0-9a-z]+)", TemplateHandler),
    (r"/task", TaskHandler),
    (r"/params", ParamsHandler),
    (r"/params/([0-9a-z]+)", ParamsHandler),
    (r"/task_log", TaskLogHandler),
]

__all__ = [
    "handlers", "base_url"
]