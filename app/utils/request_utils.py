#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

import requests
import requests.adapters
from aiohttp import ClientSession

session = requests.session()

async_session = ClientSession()

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

class AsyncRequests():
    def __init__(self, session=None):
        self.session = session or async_session

    async def get(self, url, **kwargs):
        async with self.session.get(url, **kwargs) as resp:
            # res = await resp
            print(await resp.text())
            return resp

    async def post(self, url, **kwargs):
        async  with self.session.post(url, **kwargs) as resp:
            await resp

    async def put(self, url, **kwargs):
        async with self.session.put(url, **kwargs) as resp:
            await resp

    async def delete(self, url, **kwargs):
        async with self.session.delete(url, **kwargs) as resp:
            await resp

    async def fetch(self):
        self.session


requests = Requests()
async_requeste = AsyncRequests()
if __name__ == '__main__':
    # res = requests.get("http://www.baidu.com")
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_requeste.get("http://www.baidu.com"))
    loop.close()
