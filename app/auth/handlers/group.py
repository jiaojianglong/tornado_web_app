#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.auth.auth_handler import PermissionHandler
from app.auth.models.user import GroupModel, UserModel


class GroupHandler(PermissionHandler):
    _datamodel_ = GroupModel

    def get(self):
        groupname = self.get_argument("groupname", "")
        query = self._datamodel_.query.filter(
            self._datamodel_.groupname.like("%{}%".format(groupname)),
        )
        groups = self.page.query_by_page(query)
        self.set_response(data=self.to_dict(groups))

    def post(self):
        groupname = self.get_json_argument("groupname")
        sources = self.get_json_argument("sources", [])
        users = self.get_json_argument("users", [])

        group = self._datamodel_(groupname=groupname, sources=sources)

        if users:
            users = UserModel.query.filter(
                UserModel.username.in_(users),
            ).all()
            group.users = users

        self.db_session.add(group)
        self.db_session.commit()
        self.set_response(data=self.to_dict(group))

    def put(self, id):
        groupname = self.get_json_argument("groupname")
        sources = self.get_json_argument("sources", [])
        users = self.get_json_argument("users", [])

        group = self._datamodel_.query.get(id)

        group.groupname = groupname
        group.sources = sources
        if users:
            users = UserModel.query.filter(
                UserModel.username.in_(users),
            ).all()
            group.users = users

        self.db_session.add(group)
        self.db_session.commit()
        self.set_response(data=self.to_dict(group))
