#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Entries as classes
"""

from src.DB.Model import Model


class Stock(Model):
    table = 'stock'  # table name is stock
    fields = ['id', 'ticker', 'name', 'exchange', 'pv_close', 'pv_volume']


class Quote(Model):
    table = 'quote'
    fields = ['id', 'price', 'volume', 'time']


class M_Stock(Model):
    table = 'mini_stock'  # table name is stock
    fields = ['id', 'ticker', 'name', 'pv_close', 'pv_volume']


class M_Quote(Model):
    table = 'mini_quote'
    fields = ['id', 'price', 'time']


class Portfolio(Model):
    table = 'portfolio'
    fields = ['id', 'name', 'init_fund', 'strategy']


class Scoreboard(Model):
    table = 'scoreboard'
    fields = ['portfolio', 'date', 'balance']


class Position(Model):
    # todo: 记录每天成绩
    table = 'position'
    fields = ['portfolio', 'stock', 'shares', 'avg_cost', 'total_cost', 'aggr_cost']


class Transaction(Model):
    table = 'transaction'
    fields = ['id', 'time', 'position', 'action', 'shares', 'price', 'total']


class Indicator(Model):
    # doto: not done
    table = 'quote'
    fields = ['stock', 'time', 'change', 'volume', 'moving average', 'MACD', 'KDJ', 'Boll', 'W&R', 'VR']


if __name__ == '__main__':
    # StockDAL.ECHO = False
    # first = Portfolio(name='MACD', strategy='MACD')
    # Portfolio.add([first])
    # st = Stock(ticker='LVS')
    # Stock.add([st])
    # st['pv_close'] = 333123
    # print st.working_dict(), st.query_dict()
    # st.save()
    # config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")
    # config_args = dict(zip(['host', 'user', 'passwd', 'database'],
    #                     [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
    # src.DB.NewDAL.create_engine(**config_args)
    for stock in Stock.get():
        print stock
    pass
