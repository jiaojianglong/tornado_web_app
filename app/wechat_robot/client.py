import socket
import time

from tornado import gen
from tornado.tcpclient import TCPClient
from tornado.queues import Queue
from threading import Thread

from app.wechat_robot.message import message
from app.wechat_robot.parser import Parser


class TcpClient(object):
    def __init__(self, host, accept_port, send_port):
        self.host = host
        self.accept_port = accept_port
        self.send_port = send_port
        self.accept_stream = None
        self.send_stream = None
        self.delimiter = b"|EOF|"
        self.decollator = "*|*"
        self.send_queue = []
        self.accept_queue = []

    @gen.coroutine
    def start_accept(self):
        self.accept_stream = yield TCPClient().connect(self.host, self.accept_port, af=socket.AF_INET)
        while True:
            print("开始接收消息")
            res = yield self.accept_stream.read_until(self.delimiter)
            print(res)
            yield self.handle_message(res.decode("gbk").rstrip("|EOF|"))

    @gen.coroutine
    def start_send(self):
        self.send_stream = yield TCPClient().connect(self.host, self.send_port, af=socket.AF_INET)
        while True:
            if len(self.send_queue):
                msg = self.send_queue.pop()
                print("发送消息：" + str(msg))
                if msg.get("get_return"):
                    self.send_stream.write(msg.get("msg").encode("gbk"))
                    res = yield self.send_stream.read_until(self.delimiter)
                    res = res.decode("gbk").rstrip("|EOF|")
                    res = {"res": res, "id": msg.get("id")}
                    print(res)
                    self.accept_queue.append(res)
                else:
                    self.send_stream.write(msg.get("msg").encode("gbk"))
            yield gen.sleep(0.5)

    def send_and_return(self, msg):
        msg = {"msg": self.decollator.join(msg), "get_return": True, "id": time.time()}
        self.send_queue.append(msg)
        while True:
            for res in self.accept_queue:
                if res.get("id") == msg.get("id"):
                    self.accept_queue.remove(res)
                    return res.get("res")
            time.sleep(0.5)

    def send(self, msg):
        msg = {"msg": self.decollator.join(msg)}
        self.send_queue.append(msg)

    def get_friends(self):
        res = self.send_and_return(["Friend"])
        friends = Parser.get_friends(res)
        return friends

    def send_message(self, to, message):
        self.send(["Text", to, message])

    @gen.coroutine
    def handle_message(self, msg):
        print("接收消息：", msg)
        try:
            msg = message(self, msg)
            if msg:
                Thread(target=msg.handle).start()
        except Exception as e:
            print(e)

