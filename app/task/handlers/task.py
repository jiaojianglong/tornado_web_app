#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.auth.auth_handler import PermissionHandler
from app.task.models.task import Task


class TaskHandler(PermissionHandler):
    _datamodel_ = Task

    def get(self):
        name = self.get_argument("name", "")
        query = self._datamodel_.query.filter(
            self._datamodel_.name.like("%{}%".format(name)),
        ).order_by(
            self._datamodel_.updatetime.desc()
        )
        tasks = self.page.query_by_page(query)
        self.set_response(data=self.to_dict(tasks))

    def post(self):
        "执行任务"
        params = self.get_json_argument_all()

        template = self._datamodel_.create_new(params)
        template.user = self.current_user
        self.db_session.add(template)
        self.db_session.commit()
        self.set_response(data=self.to_dict(template))