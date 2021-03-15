from .text_message import TextMessage

category_dict = {
        "1": TextMessage,
        "3": "picture",
        "37": "addfriend",
        "34": "voice",
        "42": "wecard",
        "43": "vedio",
        "47": "emoticon",
        "49": "file",
        "10000": "notice",
    }


def message(client, msg):
    msg_list = msg.split("*|*")
    if msg_list[0] == "Success":
        print("消息监听端口连接成功")
    if msg_list[0] == "Messg":
        return category_dict.get(msg_list[1])(client, msg)
