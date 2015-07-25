#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
entries as classes
"""

import urllib2
import urllib
import json
import datetime

import DAL


# unicode to integer (unit: cent)
def unicode2int(unicode_str):
    tmp = unicode_str.replace('.', '')
    int_num = int(tmp)
    return int_num


def int2float(int_num):
    pass


# governing class for all entries. this is a dict
class Entry(dict):
    def __init__(self, **kw):
        for k in kw:
            self[k] = kw[k]

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Entry' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class Stock(Entry):
    def __init__(self, **kw):
        if 'ticker' not in kw:
            raise Exception
        super(Stock, self).__init__(**kw)

    def __str__(self):
        return 'Stock object (%s)' % self.ticker
    __repr__ = __str__

    #
    def update(self):
        dal_instance = DAL.StockDAL()
        kw = {}
        for key in self.keys():
            kw[key] = self[key]
        dal_instance.update('stock_list', _id=self.id, **kw)

    def add(self):
        dal_instance = DAL.StockDAL()
        kw = {}
        for key in self.keys():
            kw[key] = self[key]
        dal_instance.insert_into('stock_list', **kw)

    def update_company_info(self):
        # get company info and stores in db
        # build query url for api
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from yahoo.finance.quote where symbol in ('"
        yql_query = yql_query + self.ticker + "')"
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) +\
            "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
        # get data
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)
        self['name'] = data['query']['results']['quote']['Name']
        self['exchange'] = data['query']['results']['quote']['StockExchange']
        self['pv_close'] = unicode2int(data['query']['results']['quote']['LastTradePriceOnly'])
        self['pv_volume'] = data['query']['results']['quote']['Volume']
        # update
        self.update()

    # 语句
    @staticmethod
    def get(**args):
        private_dal_instance = DAL.StockDAL()
        results = private_dal_instance.select_from('stock_list', **args)
        stocks = []
        for entry in results:
            stock = Stock(id=entry[0], ticker=entry[1], name=entry[2], exchange=entry[3], pv_close=entry[4], pv_volume=entry[5])
            stocks.append(stock)
        return stocks

    @staticmethod
    def rm():
        pass


class Quote(Entry):
    def __init__(self, **kw):
        super(Quote, self).__init__(**kw)

    def __str__(self):
        return 'Quote object (%s: $%s)' % (self.ticker, self.price)
    __repr__ = __str__

    def update(self):
        dal_instance = DAL.StockDAL()
        kw = {}
        for key in self.keys():
            kw[key] = self[key]
        dal_instance.update('stock_quote', _id=self.id, **kw)

    def add(self):
        dal_instance = DAL.StockDAL()
        kw = {}
        for key in self.keys():
            if key != 'ticker':  # table quote has no column ticker
                kw[key] = self[key]
        dal_instance.insert_into('stock_quote', **kw)

    @staticmethod
    def get(**args):
        private_dal_instance = DAL.StockDAL()
        results = private_dal_instance.select(
                    "select * from stock_quote \
                    left join stock_list \
                    on stock_quote.id = stock_list.id")
        quotes = []
        for entry in results:
            quote = Quote(id=entry[0], price=entry[1], volume=entry[2], time=entry[3], ticker=entry[5])
            quotes.append(quote)
        return quotes

    @staticmethod
    def rm_after_market_quotes():
        after_market_entries = {}
        for quote in Quote.get():
            if quote.time.weekday() > 4 or\
                    (quote.time.hour() > 4 and quote.time.hour() < 21) or\
                    (quote.time.hour() == 21 and quote.time.minute() < 30):
                after_market_entries[(quote.id, quote.time)] = quote.time
        for entry in after_market_entries.keys():
            #rm()
            pass

    @staticmethod
    def rm():
        pass


class Portfolio(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Portfolio Entry (%s)' % self.name
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


class Transaction(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Transaction Entry (%s)' % self.id
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


class Indicator(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Indicator Entry (%s)' % self.ticker
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
    Quote.rm_after_market_quotes()
    #st = Stock(ticker='BABA')
    #st.add()
    #st.update_company_info()

    #fb.name = 'Facebook'
    #fb.pv_close = 12345

    #yoku.pv_close = '20.80'
    #yoku.update()
    #Stock.get(ticker='YOKU')
    pass
