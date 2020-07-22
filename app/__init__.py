#!usr/bin/env python
# -*- coding:utf-8 -*-

import logging

import tornado.web
import tornado.options
from settings import APPS


def define_options():
    """命令行参数定义"""
    options = tornado.options.options
    options.define("port", default=8888, type=int, help="run with this port")
    options.define("apps", default=APPS, type=str, help="which apps to run")


def make_app():
    """初始化 Application"""
    define_options()
    tornado.options.options.parse_command_line()
    handlers = load_headlers()
    app = tornado.web.Application(
        handlers=handlers,
    )

    app.listen(tornado.options.options.port)

    return app


def load_headlers():
    handlers = []
    apps = tornado.options.options.apps
    apps = apps.split(",")
    for app in apps:
        try:
            app_module = __import__(app)
            handlers.extend(app_module.handlers)
        except NameError:
            logging.error("app init error: {}".format(app))
    return handlers
