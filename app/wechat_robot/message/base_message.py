class BaseMessage(object):
    category_dict = {
        "1": "text",
        "3": "picture",
        "37": "addfriend",
        "34": "voice",
        "42": "wecard",
        "43": "vedio",
        "47": "emoticon",
        "49": "file",
        "10000": "notice",
    }

    def __init__(self, client, msg):
        self.client = client
        self.msg = msg
        self.decollator = "*|*"
        self.type = None
        self.category = None
        self.from_ = None
        self.is_group = False
        self.member = None
        self.text = None
        self.parse_message()

    def parse_message(self):
        msg_list = self.msg.split(self.decollator)
        self.type = msg_list[0]
        if self.type == "Success":
            self.text = msg_list[1]
            return
        self.category = self._get_category(msg_list[1])
        self.from_ = msg_list[3]
        self.text = msg_list[6]
        if msg_list[4] != "_":
            self.is_group = True
            self.member = msg_list[4]

    def _get_category(self, num):
        return self.category_dict.get(num, "None")

    def handle(self):
        raise Exception

    def reply_text(self, text):
        self.client.send(["Text", self.from_, text])