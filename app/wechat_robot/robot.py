#!usr/bin/env python
# -*- coding:utf-8 -*-

from settings import WXBot
from app.wechat_robot.client import TcpClient


class Robot():
    def __init__(self):
        self.connect = self.connect_robot()

    def connect_robot(self):
        tcp_client = TcpClient(
            WXBot.get("host"),
            WXBot.get("accept_port"),
            WXBot.get("send_port"),
        )
        tcp_client.start_accept()
        tcp_client.start_send()
        return tcp_client

    def send_message(self, to, message):
        self.connect.send(["Text", to, message])

    def send_image(self, to, path):
        self.connect.send(["Image", to, path])

    def send_file(self, to, path):
        self.connect.send(["File", to, path])

    def send_card(self, to, card_id):
        self.connect.send(["Card", to, card_id])

    def send_xml(self, to, title, image, description, url):
        self.connect.send(["Xml", to, title, image, description, url])

    def get_friends(self):
        message = self.connect.send_and_return(["Friend"])
        friend_str_list = message.split("Frien")
        friends = []
        for friend_str in friend_str_list:
            if not friend_str:
                continue
            friend_info_list = friend_str.split("*|*")
            friend = {
                "type": friend_info_list[1],
                "wxid": friend_info_list[2],
                "name": friend_info_list[4],
                "nickname": friend_info_list[5]
            }
            friends.append(friend)
        return friends
