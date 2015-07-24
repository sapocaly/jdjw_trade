#!usr/bin/env python
# -*- Coding: utf-8 -*-

"""
Stock data module
given a list of stocks
gets data from Yahoo Finance
and records data in table stock_data
"""

import mysql.connector
import urllib2
import urllib
import json


# quotes to be written in table stock_quote
class Quote(object):

    def __init__(self, ticker, price, volume):
        self.ticker = ticker
        self.price = price
        self.volume = volume


# fetcher machine that gets quotes from Yahoo Finance
class Fetcher():

    def __init__(self):
        # get stock list from table stock_list, stores in self.ticker_list
        conn = mysql.connector.connect(host='www.jdjw.org', user='jdjw',
                                       password='10041023', database='master_db')  # didn't include use_unicode=True
        cursor = conn.cursor()
        cursor.execute('select ticker from stock_list')
        values = cursor.fetchall()
        self.ticker_list = []
        for ticker in values[0]:
            self.ticker_list.append(ticker)
        cursor.close()
        conn.close()

    def get_yql_query(self):
        # converts list of stock into url for yql_query
        yql_query = "select * from yahoo.finance.quote where symbol in ('"
        tickers = "','".join(self.ticker_list)
        yql_query = yql_query + tickers + "'')"
        return yql_query

    def get_prices(self):
        # base url
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from yahoo.finance.quote where symbol in "
        #tickers = "','".join(self.ticker_list)
        yql_query = yql_query + "('YHOO','AAPL')"
        ## connect all url parts (including options)
        ##yql_url = baseurl + urllib.urlencode({'q': self.get_yql_query}) +\
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) +\
            "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
        # get data
        #print yql_url
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)
        quote_data = data['query']['results']['quote']
        self.quotes = []
        for q in quote_data:
            self.quotes.append(Quote(q['symbol'],
                                     q['LastTradePriceOnly'],
                                     q['Volume']))
            #print self.quotes[0].ticker

    def record_data(self):
        pass

fetcher = Fetcher()
fetcher.get_prices()
