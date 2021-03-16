#!usr/bin/env python
# -*- coding:utf-8 -*-
from app.wechat_robot import wechat_robot
from app.task.robot import BaseRobot

class WeChatRobot(BaseRobot):
    wechat_robot = wechat_robot