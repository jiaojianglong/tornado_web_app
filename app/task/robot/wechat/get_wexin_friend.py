#!usr/bin/env python
# -*- coding:utf-8 -*-
from app.task.robot.wechat import WeChatRobot
class WeChatFriends(WeChatRobot):
    """
describe: 获取微信好友
params:[]
    """
    def run(self):
        friends = self.wechat_robot.get_friends()
        self.logger.info(friends)
        return friends