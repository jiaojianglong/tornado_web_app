#!usr/bin/env python
# -*- coding:utf-8 -*-
from app.wechat_robot import tcp_client
from app.task.robot import BaseRobot

class WeChatRobot(BaseRobot):
    WeChat = tcp_client