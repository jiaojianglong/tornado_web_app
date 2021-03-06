#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.auth.auth_handler import PermissionHandler
from app.task.models.params import Params


class ParamsHandler(PermissionHandler):
    _datamodel_ = Params

    def get(self):
        template_id = self.get_argument("template_id", "")
        query = self._datamodel_.query.filter(
            self._datamodel_.template_id==template_id
        ).order_by(
            self._datamodel_.updatetime.desc()
        )
        params = self.page.query_by_page(query)
        self.set_response(data=self.to_dict(params))

    def post(self):
        params = self.get_json_argument_all()

        params = self._datamodel_.create_new(params)
        self.db_session.add(params)
        self.db_session.commit()
        self.set_response(data=self.to_dict(params))

    def put(self, id):
        params = self.get_json_argument_all()

        params_obj = self._datamodel_.get_or_404(id)
        params_obj = params_obj.update(params)
        self.db_session.add(params_obj)
        self.db_session.commit()
        self.set_response(data=self.to_dict(params_obj))