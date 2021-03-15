#!usr/bin/env python
# -*- coding:utf-8 -*-

from app.task.robot.wechat import WeChatRobot

class SendMessageRobot(WeChatRobot):
    """
describe: 发送微信信息
params:[{
"type": "str",
"describe": "用户微信id",
"name": "wxid",
"required": true
},{
"type": "str",
"describe": "信息内容",
"name": "message",
"required": true
}]
    """
    def run(self):
        wxid = self.params.get("wxid")
        message = self.params.get("message")
        self.WeChat.send_message(wxid, message)