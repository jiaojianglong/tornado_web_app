#!usr/bin/env python
# -*- coding:utf-8 _*-

import logging

import tornado.ioloop
import tornado.options
import tornado.web

from app import make_app
from utils.log import format_log


def main():
    format_log()
    make_app()
    logging.info("程序启动 listen:{}".format(tornado.options.options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
