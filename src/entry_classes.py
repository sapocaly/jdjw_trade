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

    table = None
    fields = None

    # get key, vales from **args
    def __init__(self, **args):
        for k in args:
            self[k] = args[k]
        self.dal_instance = None

    #def __getattr__(self, key):
    #    if key != 'dal_instance':  # todo: better way to 防止dal_instance进入dict，下同
    #        try:
    #            return self[key]
    #        except KeyError:
    #            raise AttributeError(r"'Entry' object has no attribute '%s'" % key)
#
    #def __setattr__(self, key, value):
    #    if key != 'dal_instance':
    #        self[key] = value

    def call_dal_instance(self):
        if self.dal_instance is None:
            self.dal_instance = DAL.StockDAL()

    def add(self):
        self.call_dal_instance()
        self.dal_instance.insert_into(self.__class__.table, **self)

    # todo: 两套数据，一套用户输入一套数据库操作 (暂时不做)
    # todi: 增加时间确定
    def save(self):
        self.call_dal_instance()
        self.dal_instance.update(self.__class__.table, _id=self['id'], **self)

    @classmethod
    def get(cls, **args):
        private_dal_instance = DAL.StockDAL()
        selection = private_dal_instance.select_from(cls.table, **args)
        # 获取entry信息，创建新instance，initialize，生成list
        results = [cls(**dict(zip(cls.fields, entry))) for entry in selection]
        return results

    # remove, 即可传入多个Entry也可传入list of Entry
    @classmethod
    def rm(cls, *args):
        private_dal_instance = DAL.StockDAL()
        for arg in args:
            if isinstance(arg, Entry):
                private_dal_instance.delete_from(cls.table, **arg)
            elif isinstance(arg, list):
                for x in arg:
                    private_dal_instance.delete_from(cls.table, **x)


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

    @classmethod
    def get():
        pass


class Transaction(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Transaction Entry (%s)' % self['id']
    #__repr__ = __str__

    @classmethod
    def get():
        pass


class Indicator(Entry):
    def __init__(self):
        pass

    #def __str__(self):
    #    return 'Indicator Entry (%s)' % self.ticker
    #__repr__ = __str__

    @classmethod
    def get():
        pass


if __name__ == '__main__':
    Quote.rm_after_market_quotes()
    #ticker_list = []
    #for ticker in ticker_list:
    #    st = Stock(ticker=ticker)
    #    st.add()
    #    st = Stock.get(ticker=ticker)[0]
    #    st.update_company_info()

    pass
