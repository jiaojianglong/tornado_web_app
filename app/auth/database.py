#!usr/bin/env python
# -*- coding:utf-8 _*-
# author: jiaojianglong
# @time: 2020/07/14

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import weakref
from sqlalchemy_serializer import SerializerMixin
from app.settings import DB_INFO
from app.errors import NotFoundError

Base = declarative_base()
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' %
                       (DB_INFO.get("DB_USER"),
                        DB_INFO.get("DB_PWD"),
                        DB_INFO.get("DB_HOST"),
                        DB_INFO.get("DB_PORT"),
                        DB_INFO.get("DB_NAME")),
                       echo=False,
                       pool_recycle=3 * 60,
                       )

Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base.query = Session.query_property()


class BaseModel(Base, SerializerMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    createtime = Column(DateTime, default=func.now(), comment='创建时间')
    updatetime = Column(DateTime, default=func.now(), onupdate=func.now(), comment='修改时间')
    is_enable = Column(Boolean, default=True, comment="是否可用")
    serialize_only = ("id", "createtime", "updatetime", "is_enable")

    @classmethod
    def get_or_404(cls, id: str):
        item = cls.query.get(id)
        if item is None:
            raise NotFoundError("{}:{}".format(cls.__tablename__, id))

        if not item.is_enable:
            raise NotFoundError("已删除:{}:{}".format(cls.__tablename__, id))
        return item

    @classmethod
    def remove(cls, id: str):
        item = cls.get_or_404(id)
        item.is_enable = False
        return item
