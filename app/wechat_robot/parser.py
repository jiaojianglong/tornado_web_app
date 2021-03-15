#!usr/bin/env python
# -*- coding:utf-8 -*-

class Parser():

    @classmethod
    def get_friends(cls, message):
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

if __name__ == '__main__':
    friend_str = "Frien*|*3*|*jtr593472435*|*v3_020b3826fd0301000000000019e20568e7754a000000501ea9a3dba12f95f6b60a0536a1adb6e9816ec86159134e9bc73*|*Arthur*|*Arthur*|*_Frien*|*3*|*wxid_55y4nuy2ycv612*|*_*|*WAYNE*|*周游小号*|*_Frien*|*3*|*wxid_724gkom139sr21*|*_*|*LIIIIIIIIII*|*李恬楚*|*_Frien*|*3*|*wxid_au9475jj8ltn22*|*_*|*木子心木木??*|*_*|*_Frien*|*3*|*wxid_lkjy3t6spc4u22*|*v3_020b3826fd03010000000000b2ad19839eeb0c000000501ea9a3dba12f95f6b60a0536a1adb6e9816ec86159134e9bc73*|*焦江龙*|*_*|*_Frien*|*3*|*wxid_x989hhophrwb22*|*_*|*平安3*|*_*|*_Frien*|*3*|*filehelper*|*v3_020b3826fd03010000000000cac8376c3325a0000000501ea9a3dba12f95f6b60a0536a1adb6e9816ec86159134e9bc73*|*文件传输助手*|*_*|*_Frien*|*2*|*gh_25d9ac85a4bc*|*_*|*微信游戏*|*_*|*_Frien*|*2*|*gh_8a58114a8b2c*|*_*|*地道风物*|*_*|*_Frien*|*3*|*newsapp*|*_*|*_*|*_*|*_Frien*|*3*|*qqmail*|*_*|*QQ邮箱提醒*|*_*|*_"
    res = Parser.get_friends(message=friend_str)
    print(res)