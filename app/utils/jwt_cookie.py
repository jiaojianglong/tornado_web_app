#!usr/bin/env python
# -*- coding:utf-8 -*-

import jwt
from app.settings import JWT_SECRET


class JWT():
    headers = {"alg": "HS256", "typ": "JWT"}
    key = JWT_SECRET
    algorithm = 'HS256'
    @classmethod
    def get_cookie(cls, payload: dict):
        jwt_cookie = jwt.encode(payload=payload,
                                key=cls.key,
                                algorithm=cls.algorithm,
                                headers=cls.headers).decode('utf-8')
        return jwt_cookie

    @classmethod
    def get_payload(cls, cookie):
        try:
            payload = jwt.decode(cookie, key=cls.key, algorithm=cls.algorithm, headers=cls.headers)
            return payload
        except:
            return {}

if __name__ == '__main__':
    cookie = JWT.get_cookie({"aaa":"bbb"})
    print(cookie)
    print(JWT.get_payload(cookie[:-3]))