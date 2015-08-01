#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model class for all entries
"""

from src.DB.NewDAL import *


# governing class for all entries. this is a dict
class Entry(dict):
    table = None
    fields = None
    index = None

    # get key, vales from **args
    def __init__(self, **args):
        super(Entry, self).__init__(**args)
        # 存一份用户不修改的信息
        for kw in args.keys():
            self['_' + kw] = args[kw]

    def _query_dict(self):
        query_dict = {}
        for key in self.keys():
            if key[0] == '_':
                query_dict[key] = self[key]
        return query_dict

    def _working_dict(self):
        working_dict = {}
        for key in self.keys():
            if key[0] != '_':
                working_dict[key] = self[key]
        return working_dict

    # todo: 同步
    def save(self):
        try:
            update(self.__class__.table, **dict(self._query_dict(), **self._working_dict()))
        except Exception as e:
            print 'Saving failed: ', str(self), e

    @classmethod
    def search(cls, **args):
        try:
            selection = select_from(cls.table, **args)
            # 获取entry信息，创建新instance，initialize，生成list
            return [cls(**dict(zip(cls.fields, entry))) for entry in selection]
        except Exception as e:
            print 'Getting failed: ', str(args), e

    @classmethod
    def add(cls, lst):
        # 是否需要保持事务性?
        with connection():
            for entry in lst:
                try:
                    insert_into(cls.table, **entry._working_dict())
                except Exception as e:
                    print 'Adding failed: ', str(entry), e

    # remove, 即可传入多个Entry也可传入list of Entry
    @classmethod
    def rm(cls, lst):
        with connection():
            for entry in lst:
                try:
                    delete_from(cls.table, **entry._working_dict())
                except Exception as e:
                    print 'Removing failed: ', str(entry), e


if __name__ == '__main__':
    config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")
    config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                           [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
