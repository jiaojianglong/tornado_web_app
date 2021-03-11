#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.auth.auth_handler import PermissionHandler
from app.task.models.task import Task
from app.task.models.params import Params


class TaskHandler(PermissionHandler):
    _datamodel_ = Task

    def get(self):
        template_id = self.get_argument("template_id", "")
        query = self._datamodel_.query.filter(
            self._datamodel_.template_id==template_id
        ).order_by(
            self._datamodel_.updatetime.desc()
        )
        tasks = self.page.query_by_page(query)
        self.set_response(data=self.to_dict(tasks))

    def post(self):
        "执行任务 将任务保存到数据库 等待执行"
        params = self.get_json_argument_all()

        params_obj = Params.get_or_404(params.get("params_id"))

        task = self._datamodel_.create_new(params_obj, self.current_user)
        self.db_session.add(task)
        self.db_session.commit()
        self.set_response(data=self.to_dict(task))