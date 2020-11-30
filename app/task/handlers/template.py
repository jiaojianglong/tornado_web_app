#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.auth.auth_handler import PermissionHandler
from app.task.models.template import TaskTemplate


class TemplateHandler(PermissionHandler):
    _datamodel_ = TaskTemplate

    def get(self):
        name = self.get_argument("name", "")
        query = self._datamodel_.query.filter(
            self._datamodel_.name.like("%{}%".format(name)),
        ).order_by(
            self._datamodel_.updatetime.desc()
        )
        actions = self.page.query_by_page(query)
        self.set_response(data=self.to_dict(actions))

    def post(self):

        params = self.get_json_argument_all()

        template = self._datamodel_.create_new(params)
        template.user = self.current_user
        self.db_session.add(template)
        self.db_session.commit()
        self.set_response(data=self.to_dict(template))

    def put(self, id: str):
        template = self._datamodel_.get_or_404(id)
        params = self.get_json_argument_all()
        update_list = ["description", "actions", "name"]
        template = self.update_all(template, params, update_list)
        self.db_session.add(template)
        self.db_session.commit()
        self.set_response(data=self.to_dict(template))