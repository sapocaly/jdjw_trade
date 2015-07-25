#!usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Stock data module
reads stock list from database
gets data from Yahoo Finance
and records data in table stock_data
"""

import urllib2
import urllib
import json
import DAL
import entry_classes


# unicode to integer (unit: cent)
def unicode2int(unicode_str):
    tmp = unicode_str.replace('.', '')
    int_num = int(tmp)
    return int_num


def int2float(int_num):
    pass


# gets quotes from Yahoo Finance
def fetch_quotes():
    # read from db
    results = entry_classes.Stock.get()
    tickers = [stock.ticker for stock in results]

    # build query url for api
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from yahoo.finance.quote where symbol in ('"
    ticker_url = "','".join(tickers)
    yql_query = yql_query + ticker_url + "')"
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) +\
        "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
    #print yql_url

    # get data
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    quote_data = data['query']['results']['quote']

    quotes = [entry_classes.Quote(ticker=q['symbol'],
                                  price=unicode2int(q['LastTradePriceOnly']),
                                  volume=int(q['Volume']))
              for q in quote_data]
    print quotes

    # todo: write results into db
    for q in quotes:
        q.add()

if __name__ == '__main__':
    fetch_quotes()
    #print unicode2int('123.234')
