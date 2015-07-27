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

    def save(self):
        dal_instance = StockDAL()
        try:
            dal_instance.update(cls.table, _id=x['id'], **self)
        except Exception as e:
            print 'Saving failed: ', str(self),  e
        finally:
            dal_instance.close()

    @classmethod
    def get(cls, **args):
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
                dal_instance.insert_into(cls.table, **entry)
            except Exception as e:
                print 'Adding failed: ', str(entry), e
        dal_instance.close()
    # todo: 两套数据，一套用户输入一套数据库操作 (暂时不做)

    # remove, 即可传入多个Entry也可传入list of Entry
    @classmethod
    def rm(cls, lst):
        dal_instance = StockDAL()
        for entry in lst:
            try:
                dal_instance.delete_from(cls.table, **entry)
            except Exception as e:
                print 'Removing failed: ', str(entry), e
        dal_instance.close()
