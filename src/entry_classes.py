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

    # todo:内存交互method
    def __init__(self, ticker, name=None, exchange=None, pv_close=None, pv_volume=None):
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.pv_close = pv_close
        self.pv_volume = pv_volume
        self.dal_instance = None  # DAL 实例

    def __str__(self):
        return 'Stock object (%s)' % self.ticker
    __repr__ = __str__

    def update(self):
        pass

    @staticmethod
    def add(stock):
        private_dal_instance = DAL.StockDAL()
        private_dal_instance.insert_into('stock_list',
                                         ticker=stock.ticker, name=stock.name,
                                         exchange=stock.exchange, pv_close=stock.pv_close,
                                         pv_volume=stock.pv_close)

    @staticmethod
    def get(**args):
        private_dal_instance = DAL.StockDAL()
        results = private_dal_instance.select_from('stock_list', **args)
        stocks = []
        for entry in results:
            stock = Stock(entry[1], entry[2], entry[3], entry[4], entry[5])
            stocks.append(stock)
        return stocks

    @staticmethod
    def rm():
        pass


class Quote(object):
    __metaclass__ = EntryMetaclass

    def __init__(self, ticker, price, volume):
        self.ticker = ticker
        self.price = price
        self.volume = volume
        self.dal_instance = None

    def __str__(self):
        return 'Quote object (%s: $%s)' % (self.ticker, self.price)
    __repr__ = __str__

    def update(self):
        pass

    @staticmethod
    def add():
        pass

    @staticmethod
    def get():
        pass

    @staticmethod
    def rm():
        pass


class Portfolio(object):
    __metaclass__ = EntryMetaclass

    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Portfolio object (%s)' % self.name
    #__repr__ = __str__

    def update(self):
        pass

    @staticmethod
    def add():
        pass

    @staticmethod
    def get():
        pass

    @staticmethod
    def rm():
        pass


class Transaction(object):
    __metaclass__ = EntryMetaclass

    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Transaction object (%s)' % self.id
    #__repr__ = __str__

    def update(self):
        pass

    @staticmethod
    def add():
        pass

    @staticmethod
    def get():
        pass

    @staticmethod
    def rm():
        pass


class Indicator(object):
    __metaclass__ = EntryMetaclass

    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Indicator object (%s)' % self.ticker
    #__repr__ = __str__

    def update(self):
        pass

    @staticmethod
    def add():
        pass

    @staticmethod
    def get():
        pass

    @staticmethod
    def rm():
        pass

if __name__ == '__main__':
    #appl = Stock('APPL', 'Apple, Inc.', 'NYSE')
    #Stock.add(appl)
    Stock.get(ticker='AAPL')
