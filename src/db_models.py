#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
entries as classes
"""

import urllib2
import urllib
import json

from entry import Entry
from DAL import StockDAL


# unicode to integer (unit: cent)
def unicode2int(unicode_str):
    tmp = unicode_str.replace('.', '')
    int_num = int(tmp)
    return int_num


def int2float(int_num):
    pass


class Stock(Entry):

    table = 'stock'  # table name is stock
    fields = ['id', 'ticker', 'name', 'exchange', 'pv_close', 'pv_volume']

    def __init__(self, **args):
        super(Stock, self).__init__(**args)

    def __str__(self):
        return 'Stock object (%s)' % self['ticker']
    __repr__ = __str__

    # todo: 移到上面一层 （逻辑层）
    def update_company_info(self):
        # get company info and stores in db
        # build query url for api
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from yahoo.finance.quote where symbol in ('"
        yql_query = yql_query + self['ticker'] + "')"
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) +\
            "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
        # get data
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)
        self['name'] = data['query']['results']['quote']['Name'][:20]
        self['exchange'] = data['query']['results']['quote']['StockExchange']
        self['pv_close'] = unicode2int(data['query']['results']['quote']['LastTradePriceOnly'])
        self['pv_volume'] = data['query']['results']['quote']['Volume']
        # update
        self.save()


class Quote(Entry):

    table = 'quote'
    fields = ['id', 'price', 'volume', 'time']

    def __init__(self, **args):
        super(Quote, self).__init__(**args)

    def __str__(self):
        return 'Quote object (ID %s: $%s)' % (self['id'], self['price'])
    __repr__ = __str__

    # todo: 移到逻辑层
    @classmethod
    def rm_after_market_quotes(cls):
        for quote in Quote.get():
            time = quote['time']
            # US East
            #if (time.weekday() > 4) or\
            #        ((time.hour() > 4 or (time.hour() == 4 and time.minute() > 0))and
            #         (time.hour() < 21 or (time.hour() == 21 and time.minute() < 30))):
            # GMT +8
            after_market_quotes = []
            if (time.weekday() == 0 and time.hour() < 4) or\
                    (time.weekday() == 5 and (time.hour() > 21 or (time.hour() == 21 and time.minute() >= 30))) or\
                    time.weekday() == 6 or\
                    ((time.hour() > 4 or (time.hour() == 4 and time.minute() > 0))and
                     (time.hour() < 21 or (time.hour() == 21 and time.minute() < 30))):
                #quote['time'] = str(time)
                after_market_quotes.append(quote)
            Quote.rm(after_market_quotes)


class Portfolio(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Portfolio Entry (%s)' % self.name
    #__repr__ = __str__


class Transaction(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Transaction Entry (%s)' % self['id']
    #__repr__ = __str__


class Indicator(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Indicator Entry (%s)' % self.ticker
    #__repr__ = __str__


if __name__ == '__main__':
    StockDAL.ECHO = False
    #Quote.rm_after_market_quotes()
    #for ticker in ticker_list:
    #    st = Stock(ticker=ticker)
    #    st.add()
    #    st = Stock.get(ticker=ticker)[0]
    #    st.update_company_info()

    pass
