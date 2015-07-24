#!usr/bin/env python
# -*- Coding: utf-8 -*-

"""
entries as classes
"""


class EntryMetaclass(type):
    pass


class Stock(object):
    __metaclass__ = EntryMetaclass

    def __init__(self, ticker, name=None, exchange=None, pv_close=None, pv_volume=None):
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.pv_close = pv_close
        self.pv_volume = pv_volume

    def update(self):
        pass

    @staticmethod
    def insert(stock):
        StockDAL.insert_into(‘stock_list’,
                             ticker=stock.ticker, name=stock.name,
                             exchange=stock.exchange, pv_close=stock.pv_close,
                             pv_volume=stock.pv_close)

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
        self.   

    def update(self):
        pass

    @staticmethod
    def insert():
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
        self.   

    def update(self):
        pass

    @staticmethod
    def insert():
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
        self.   

    def update(self):
        pass

    @staticmethod
    def insert():
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
        self.   

    def update(self):
        pass

    @staticmethod
    def insert():
        pass

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def rm():
        pass

    pass