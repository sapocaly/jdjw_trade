#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model class for all entries
"""

import urllib2
import urllib
import json
import datetime

from DAL import StockDAL


# governing class for all entries. this is a dict
class Entry(dict):

    table = None
    fields = None

    # get key, vales from **args
    def __init__(self, **args):
        for k in args:
            self[k] = args[k]
        self.dal_instance = None

    def call_dal_instance(self):
        if self.dal_instance is None:
            self.dal_instance = StockDAL()

    def close_dal(self):
        self.dal_instance.close()
        self.dal_instance = None

    def add(self):
        self.call_dal_instance()
        self.dal_instance.insert_into(self.__class__.table, **self)
        self.close_dal()

    # todo: 两套数据，一套用户输入一套数据库操作 (暂时不做)
    # todi: 增加时间确定
    def save(self):
        self.call_dal_instance()
        self.dal_instance.update(self.__class__.table, _id=self['id'], **self)
        self.close_dal()

    @classmethod
    def get(cls, **args):
        private_dal_instance = StockDAL()
        selection = private_dal_instance.select_from(cls.table, **args)
        # 获取entry信息，创建新instance，initialize，生成list
        results = [cls(**dict(zip(cls.fields, entry))) for entry in selection]
        private_dal_instance.close()
        return results

    # remove, 即可传入多个Entry也可传入list of Entry
    @classmethod
    def rm(cls, *args):
        private_dal_instance = StockDAL()
        for arg in args:
            if isinstance(arg, Entry):
                private_dal_instance.delete_from(cls.table, **arg)
            elif isinstance(arg, list):
                for x in arg:
                    private_dal_instance.delete_from(cls.table, **x)
        private_dal_instance.close()
