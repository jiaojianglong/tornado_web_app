#!usr/bin/env python
# -*- coding:utf-8 _*-

import tornado.log
import tornado.options
import logging


class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='%(color)s[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d '
                '%(levelname)s]%(end_color)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )


def format_log():
    def format_log_():
        print("format_log:", logging.getLogger().handlers)
        for logger_handler in logging.getLogger().handlers:
            logger_handler.setFormatter(LogFormatter())

    tornado.options.options.add_parse_callback(format_log_)
