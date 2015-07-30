#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entries as classes
"""

from src.DB.Entry import Entry
from src.DB.DAL import StockDAL


class Stock(Entry):
    table = 'stock'  # table name is stock
    fields = ['id', 'ticker', 'name', 'exchange', 'pv_close', 'pv_volume']

    def __init__(self, **args):
        super(Stock, self).__init__(**args)

    def __str__(self):
        return 'Stock object (%s)' % (self['ticker'])

    __repr__ = __str__


class Quote(Entry):
    table = 'quote'
    fields = ['id', 'price', 'volume', 'time']

    def __init__(self, **args):
        super(Quote, self).__init__(**args)

    def __str__(self):
        return 'Quote object (ID %s @ %s)' % (self['id'], self['time'])

    __repr__ = __str__


class Portfolio(Entry):
    table = 'portfolio'
    fields = ['id', 'name', 'init_fund', 'strategy']

    def __init__(self, **args):
        super(Portfolio, self).__init__(**args)

    def __str__(self):
        return 'Portfolio object (ID %s)' % self['id']

    __repr__ = __str__


class Scoreboard(Entry):
    table = 'scoreboard'
    fields = ['portfolio', 'date', 'balance']

    def __init__(self, **args):
        super(Scoreboard, self).__init__(**args)

    def __str__(self):
        return 'Scoreboard object (Portfolio %s)' % self['portfolio']

    __repr__ = __str__


class Position(Entry):
    # todo: 记录每天成绩
    table = 'position'
    fields = ['portfolio', 'stock', 'shares', 'avg_cost', 'total_cost', 'aggr_cost']

    def __init__(self, **args):
        super(Position, self).__init__(**args)

    def __str__(self):
        return 'Position object (Portfolio %s, Stock %s)' % (self['portfolio'], self['stock'])

    __repr__ = __str__


class Transaction(Entry):
    table = 'transaction'
    fields = ['id', 'time', 'position', 'action', 'shares', 'price', 'total']

    def __init__(self, **args):
        super(Transaction, self).__init__(**args)

    def __str__(self):
        return 'Transaction object (ID: %s)' % self['id']

    __repr__ = __str__


class Indicator(Entry):
    # doto: not done
    table = 'quote'
    fields = ['stock', 'time', 'change', 'volume', 'moving average', 'MACD', 'KDJ', 'Boll', 'W&...', 'VR']

    def __init__(self, **args):
        super(Indicator, self).__init__(**args)

    def __str__(self):
        return 'Quote object (ID %s: $%s)' % (self['id'], self['price'])

    __repr__ = __str__


if __name__ == '__main__':
    StockDAL.ECHO = False
    #first = Portfolio(name='MACD', strategy='MACD')
    #Portfolio.add([first])
    #st = Stock(ticker='LVS')
    #Stock.add([st])
    #st['pv_close'] = 333123
    #print st.working_dict(), st.query_dict()
    #st.save()

    pass
