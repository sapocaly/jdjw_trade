# coding=utf-8

"""
Indicator Calculator
"""

import datetime

from src.DB.Models import *
from src.utils.DbUtils import chop_microseconds


class iCalculator(object):
    def __init__(self, stock, time, period, frequency=1):
        """
        :param stock: str, ticker of stock
        :param time: datetime.datetime()
        :param period: int, periods of data fetched
        :param frequency: int, frequency of operation in seconds
                second: 1
                minute: 60
                hour: 3600
                day: 86400
        :return:
        """
        dal_instance
        st = Stock.search(ticker=stock)[0]
        time = time
        id = st[id]
        period = period
        frequency = frequency
        sql =
        records = dal_instance.select(sql)
        quotes = [Quote(id=quo[0], price=quo[1], volume=quo[2], time=quo[3]) for quo in records]

    def high(self, period):
        pass

    def low(self, period):
        pass

    def ma(self, period, frequency=1):
        pass

    def macd(self, short_prd, long_prd):
        pass

    def kdj(self, n):
        pass

    def boll(self):
        pass

    def wr(self):
        pass

    def vr(self):
        pass

    def record(self):
        pass
