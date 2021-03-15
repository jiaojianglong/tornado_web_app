#!usr/bin/env python
# -*- coding:utf-8 -*-


from settings import WXBot
from app.wechat_robot.client import TcpClient

tcp_client = TcpClient(
        WXBot.get("host"),
        WXBot.get("accept_port"),
        WXBot.get("send_port"),
        )
tcp_client.start_accept()
tcp_client.start_send()