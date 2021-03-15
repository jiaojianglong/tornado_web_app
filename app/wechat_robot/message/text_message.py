from app.wechat_robot.message.base_message import BaseMessage
from tornado import gen


class TextMessage(BaseMessage):
    def handle(self):
        self.reply_text(self.text)
