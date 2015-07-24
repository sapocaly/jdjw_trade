#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
entries as classes
"""

import DAL


class EntryMetaclass(type):
    pass


class Stock(object):
    __metaclass__ = EntryMetaclass

    # DAL 实例
    dal_instance = DAL.StockDAL()

    def __init__(self, ticker, name=None, exchange=None, pv_close=None, pv_volume=None):
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.pv_close = pv_close
        self.pv_volume = pv_volume

    def update(self):
        pass

    @staticmethod
    def insert_into(stock):
        Stock.dal_instance.insert_into('stock_list',
                                       ticker=stock.ticker, name=stock.name,
                                       exchange=stock.exchange, pv_close=stock.pv_close,
                                       pv_volume=stock.pv_close)

    @staticmethod
    def select_from(**args):
        Stock.dal_instance.select_from('stock_list', **args)
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def rm():
        pass

    pass


class Quote(object):
    __metaclass__ = EntryMetaclass

    def __init__(self, ):
        pass

    def update(self):
        pass

    @staticmethod
    def insert_into():
        pass

    @staticmethod
    def select_from():
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def rm():
        pass

    pass


class Portfolio(object):
    __metaclass__ = EntryMetaclass

    def __init__(self):
        pass

    def update(self):
        pass

    @staticmethod
    def insert_into():
        pass

    @staticmethod
    def select_from():
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def rm():
        pass

    pass


class Transaction(object):
    __metaclass__ = EntryMetaclass

    def __init__(self):
        pass

    def update(self):
        pass

    @staticmethod
    def insert_into():
        pass

    @staticmethod
    def select_from():
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def rm():
        pass

    pass


class Indicator(object):
    __metaclass__ = EntryMetaclass

    def __init__(self):
        pass

    def update(self):
        pass

    @staticmethod
    def insert_into():
        pass

    @staticmethod
    def select_from():
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def rm():
        pass

    pass

appl = Stock('APPL', 'Apple, Inc.', 'NYSE')
appl.insert_into(appl)
appl.select_from(ticker='APPL')
