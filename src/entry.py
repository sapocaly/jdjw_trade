#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model class for all entries
"""

from DAL import StockDAL


# governing class for all entries. this is a dict
class Entry(dict):

    table = None
    fields = None

    # get key, vales from **args
    def __init__(self, **args):
        super(Entry, self).__init__(**args)
        self.dal_instance = None

    def call_dal_instance(self):
        if self.dal_instance is None:
            self.dal_instance = StockDAL()

    #todo: 解决调用问题：何时结束connection, 需要sy写is_active方法
    def close_dal(self):
        self.dal_instance.close()
        self.dal_instance = None

    @classmethod
    def get(cls, **args):
        try:
            private_dal_instance = StockDAL()
            selection = private_dal_instance.select_from(cls.table, **args)
            # 获取entry信息，创建新instance，initialize，生成list
            results = [cls(**dict(zip(cls.fields, entry))) for entry in selection]
        finally:
            private_dal_instance.close()
        return results

    # todo: 两套数据，一套用户输入一套数据库操作 (暂时不做)
    @staticmethod
    def save(*args):
        try:
            private_dal_instance = StockDAL()
            for arg in args:
                if isinstance(arg, Entry):
                    private_dal_instance.update(arg.__class__.table, **arg)
                elif isinstance(arg, list):
                    for x in arg:
                        private_dal_instance.update(x.__class__.table, **x)
        finally:
            private_dal_instance.close()

    @staticmethod
    def add(*args):
        try:
            private_dal_instance = StockDAL()
            for arg in args:
                if isinstance(arg, Entry):
                    private_dal_instance.insert_into(arg.__class__.table, **arg)
                elif isinstance(arg, list):
                    for x in arg:
                        private_dal_instance.insert_into(x.__class__.table, **x)
        finally:
            private_dal_instance.close()

    # remove, 即可传入多个Entry也可传入list of Entry
    @staticmethod
    def rm(*args):
        try:
            private_dal_instance = StockDAL()
            for arg in args:
                if isinstance(arg, Entry):
                    private_dal_instance.delete_from(arg.__cls__.table, **arg)
                elif isinstance(arg, list):
                    for x in arg:
                        private_dal_instance.delete_from(x.__cls__.table, **x)
        finally:
            private_dal_instance.close()
