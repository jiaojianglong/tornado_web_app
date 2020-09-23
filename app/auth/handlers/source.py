#!usr/bin/env python
# -*- coding:utf-8 -*-

from app import load_headlers
from app.auth.auth_handler import PermissionHandler


class SourceHandler(PermissionHandler):
    def get(self):
        handlers = load_headlers()
        sources = [handler[0] for handler in handlers]
        self.set_response(data=sources)
