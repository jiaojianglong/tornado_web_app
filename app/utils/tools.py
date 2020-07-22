#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib


def md5(val: str):
    hl = hashlib.md5()
    hl.update(val.encode(encoding='utf-8'))
    return hl.hexdigest()


if __name__ == '__main__':
    print(md5("jiao123456"))
