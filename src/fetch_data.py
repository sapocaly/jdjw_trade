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


# gets quotes from Yahoo Finance
def fetch_quotes():
    # read from db
    results = entry_classes.Stock.get()
    ticker_id_dict = {}
    for stock in results:
        ticker_id_dict[stock.ticker] = stock.id

    # build query url for api
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from yahoo.finance.quote where symbol in ('"
    ticker_url = "','".join(ticker_id_dict.keys())
    yql_query = yql_query + ticker_url + "')"
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) +\
        "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="

    # get data
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    quote_data = data['query']['results']['quote']

    # create objects
    quotes = [entry_classes.Quote(id=ticker_id_dict[q['symbol']],
                                  price=entry_classes.unicode2int(q['LastTradePriceOnly']),
                                  volume=q['Volume'])
              for q in quote_data]
    print quotes

    # write results into db
    for q in quotes:
        q.add()

if __name__ == '__main__':
    fetch_quotes()
