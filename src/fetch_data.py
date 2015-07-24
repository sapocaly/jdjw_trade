#!usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Stock data module
given a list of stocks
gets data from Yahoo Finance
and records data in table stock_data
"""

import urllib2
import urllib
import json


class Quote(object):

        def __init__(self, ticker, price, volume):
            self.ticker = ticker
            self.price = price
            self.volume = volume


def get_prices(stock_list):

    # base url
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    # yql query's part of url
    yql_query = "select * from yahoo.finance.quote where symbol in" +\
        " (\'YHOO\',\"AAPL\",\"GOOG\",\"MSFT\")"
    # connect all url parts (including options)
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) +\
        "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
    # get data
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    quote_data = data['query']['results']['quote']
    quotes = []
    for q in quote_data:
        quotes.append(dict2quote(q))

    # time: data['query']['created']
    # ticker: data['query']['results']['quote'][0]['symbol']
    # price: data['query']['results']['quote'][0]['LastTradePriceOnly']
    # volume: data['query']['results']['quote'][0]['Volume']

    return quotes


def dict2quote(d):
    return quote(d['symbol'], d['LastTradePriceOnly'], d['Volume'])


def record_data(fetched_data):
    pass

s_list = ['YHOO', 'AAPL', 'GOOG', 'MSFT']
print(get_prices(s_list))
