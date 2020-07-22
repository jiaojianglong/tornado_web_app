#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

import requests
import requests.adapters

session = requests.session()


class Requests():
    def __init__(self, timeout=10, max_retries=3):
        self.session = requests.session()
        self.timeout = timeout
        self._max_retries = 0
        self.max_retries = max_retries

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value):
        self._max_retries = value
        adapter = requests.adapters.HTTPAdapter(max_retries=self._max_retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get(self, url, max_retries=None, **kwargs):
        if max_retries and isinstance(max_retries, int):
            self.max_retries = max_retries
        return self.session.get(url, **kwargs)

    def post(self, url, *args, max_retries=None, **kwargs):
        if max_retries and isinstance(max_retries, int):
            self.max_retries = max_retries
        return self.session.post(url, *args, **kwargs)

    def put(self, url, *args, max_retries=None, **kwargs):
        if max_retries and isinstance(max_retries, int):
            self.max_retries = max_retries
        return self.session.put(url, *args, **kwargs)

    def delete(self, url, max_retries=None, **kwargs):
        if max_retries and isinstance(max_retries, int):
            self.max_retries = max_retries
        return self.session.delete(url, **kwargs)


requests = Requests()

if __name__ == '__main__':
    res = requests.get("http://www.baidu.com")
