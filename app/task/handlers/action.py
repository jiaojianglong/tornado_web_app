#!usr/bin/env python
# -*- coding:utf-8 -*-
import importlib
import json
import re

from app.auth.auth_handler import PermissionHandler
from app.task.models.action import Action
from app.settings import ACTION_CONFIG


class ActionHandler(PermissionHandler):
    _datamodel_ = Action

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

        action = self._datamodel_(**params)
        action.user = self.current_user
        self.db_session.add(action)
        self.db_session.commit()
        self.set_response(data=self.to_dict(action))

    def put(self, id: str):
        action = self._datamodel_.get_or_404(id)
        params = self.get_json_argument_all()
        update_list = ["action_code", "params", "name"]
        action = self.update_all(action, params, update_list)
        self.db_session.add(action)
        self.db_session.commit()
        self.set_response(data=self.to_dict(action))


class ActionCodeHandler(PermissionHandler):
    """脚本信息"""

    def get(self):
        data = []
        for action_code, config in ACTION_CONFIG.items():
            module = importlib.import_module(config.get("package"))
            action_obj = getattr(module, config.get("action_class"))
            action_doc = action_obj.__doc__
            describe = re.search(r"describe:(.*)\n", action_doc).group(1)
            print(action_doc.split("params:")[1])
            params = json.loads(action_doc.split("params:")[1])
            for parameter in params:
                parameter['value'] = parameter.get("default")
            data.append({
                "action_code": action_code,
                "params": params,
                "describe": describe
            })
        self.set_response(data=data)