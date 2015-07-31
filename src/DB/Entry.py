#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model class for all entries
"""

from src.DB.DAL import StockDAL


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
        dal_instance = StockDAL()
        try:
            dal_instance.update(self.__class__.table, **dict(self._query_dict(), **self._working_dict()))
        except Exception as e:
            print 'Saving failed: ', str(self), e
        finally:
            dal_instance.close()

    @classmethod
    def search(cls, **args):
        dal_instance = StockDAL()
        try:
            selection = dal_instance.select_from(cls.table, **args)
            # 获取entry信息，创建新instance，initialize，生成list
            results = [cls(**dict(zip(cls.fields, entry))) for entry in selection]
        except Exception as e:
            print 'Getting failed: ', str(args), e
        finally:
            dal_instance.close()
            return results

    @classmethod
    def add(cls, lst):
        dal_instance = StockDAL()
        for entry in lst:
            try:
                dal_instance.insert_into(cls.table, **entry._working_dict())
            except Exception as e:
                print 'Adding failed: ', str(entry), e
        dal_instance.close()

    # remove, 即可传入多个Entry也可传入list of Entry
    @classmethod
    def rm(cls, lst):
        dal_instance = StockDAL()
        for entry in lst:
            try:
                dal_instance.delete_from(cls.table, **entry._working_dict())
            except Exception as e:
                print 'Removing failed: ', str(entry), e
        dal_instance.close()
