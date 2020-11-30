#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.task.handlers.action import ActionHandler, ActionCodeHandler
from app.task.handlers.template import TemplateHandler

base_url = "/api/v1/task"
handlers = [
    (r"/action", ActionHandler),
    (r"/action/([0-9a-z]+)", ActionHandler),
    (r"/action_code", ActionCodeHandler),
    (r"/template", TemplateHandler),
    (r"/template/([0-9a-z]+)", TemplateHandler),
]

__all__ = [
    "handlers", "base_url"
]