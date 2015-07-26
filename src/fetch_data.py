#!usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stock data module
reads stock list from database
gets data from Yahoo Finance
and records data in table stock_data
"""

import urllib2
import urllib
import json
import datetime

from DAL import StockDAL
import db_models


def db_time_format(string):
    yyyy = int(string[:4])
    MM = int(string[5:7])
    dd = int(string[8:10])
    hh = int(string[11:13])
    mm = int(string[14:16])
    ss = int(string[17:19])
    time = datetime.datetime(yyyy, MM, dd, hh, mm, ss)
    return time


def chop_microseconds(time):
    return time - datetime.timedelta(microseconds=time.microsecond)


def get_stock_list():

    # read from db
    results = db_models.Stock.get()
    ticker_id_dict = {}
    for stock in results:
        ticker_id_dict[stock['ticker']] = stock['id']
    return ticker_id_dict


# gets quotes from Yahoo Finance
def fetch_quotes(ticker_id_dict):

    # timestamp
    fetch_time = datetime.datetime.now()

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
    quotes = [db_models.Quote(id=ticker_id_dict[q['symbol']],
                                  price=db_models.unicode2int(q['LastTradePriceOnly']),
                                  volume=q['Volume'],
                                  time=fetch_time)
              for q in quote_data]

    # write results into db
    for q in quotes:
        q.add()


if __name__ == '__main__':
    StockDAL.ECHO = False
    ticker_dict = get_stock_list()
    fetch_quotes(ticker_dict)
