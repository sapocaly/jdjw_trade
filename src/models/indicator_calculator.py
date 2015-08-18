# coding=utf-8

"""
Indicator Calculator
"""

import datetime

from src.DB.DAL import StockDAL
from src.DB.Models import *
from src.utils.DbUtils import chop_microseconds


class iCalculator(object):
    time = None
    id = None
    period = None
    frequency = None
    quotes = None

    def __init__(self, stock, time, period, frequency=1, unit='second'):
        """
        :param stock: str, ticker of stock
        :param time: datetime.datetime()
        :param period: int, periods of data fetched
        :param frequency: int, frequency of operation in seconds, must be a factor of 60
        :param unit: str, either second or day
        :return:
        """
        dal_instance = StockDAL()
        self.time = time
        self.id = Stock.search(ticker=stock)[0]['id']
        self.period = period
        self.frequency = frequency
        if unit == 'second':
            beg_time = time - datetime.timedelta(0, self.period * self.frequency)
            sql = ('select * from quote where ' +
                   'id = %d and ' % self.id +
                   'mod((extract(second from "%s") - extract(second from time)), %d) = 0 and ' % (
                   self.time, self.frequency) +
                   'extract(day_second from "%s") < extract(day_second from time)' % beg_time)
        elif unit == 'day':
            sql = ''
        records = dal_instance.select(sql)
        self.quotes = [Quote(**dict(zip(Quote.fields, quo))) for quo in records]

    def price(self, index):
        price = self.quotes[index]['price']
        return price

    def high(self, start, end=period):
        prices = [quo['price'] for quo in self.quotes[start:end]]
        high = max(prices)
        return high

    def low(self, start, end=period):
        prices = [quo['price'] for quo in self.quotes[start:end]]
        low = min(prices)
        return low

    def sma(self, period):
        pass

    def macd(self, short_prd, long_prd):
        pass

    def kdj(self, k_prd=9, d_prd=3):
        record = Indicator.search(id=self.id, time=self.quotes[self.period - 1]['time'])
        k_1 = 50
        d_1 = 50
        if 'k' in record[0].keys() and record[0]['k'] > 0:
            k_1 = record[0]['k']
        if 'd' in record[0].keys() and record[0]['d'] > 0:
            d_1 = record[0]['d']
        rsv = (self.price(self.period) - self.low(self.period - 9, self.period)) / (
        self.high(self.period - 9, self.period) - self.low(self.period - 9, self.period)) * 100
        k = rsv / 3 + 2 * k_1 / 3
        d = k / 3 + 2 * d_1 / 3
        j = 3 * d - 2 * k
        return k, d, j

    def boll(self):
        pass

    def wr(self):
        pass

    def vr(self):
        pass

    def record(self):
        pass


if __name__ == '__main__':
    time = chop_microseconds(datetime.datetime(2015, 7, 31, 4, 0, 0))
    cal = iCalculator('YHOO', time, 30, 30)
