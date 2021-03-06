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

from src.DB import Entry
from src.utils import DBconfig
from src.utils.DbUtils import unicode2int, chop_microseconds
import utils.LogConstant as LogConstant

import src.DB.DAL

config = DBconfig.DBConfig("conf/jdjw_trade_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                          [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
src.DB.DAL.create_engine(**config_args)

logger = LogConstant.FETCH_DIGEST_LOGGER
logger_alert = LogConstant.FETCH_DIGEST_LOGGER_ALERT


def get_stock_list():
    # read from db
    results = Entry.Stock.get()
    ticker_id_dict = {}
    for stock in results:
        ticker_id_dict[stock['ticker']] = stock['id']
    return ticker_id_dict


# gets quotes from Yahoo Finance
def fetch_quotes(ticker_id_dict):
    global logger
    global logger_alert
    # timestamp
    start_time = datetime.datetime.now()
    fetch_time = chop_microseconds(start_time)
    count = -1
    try:
        # build query url for api
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from yahoo.finance.quote where symbol in ('"
        ticker_url = "','".join(ticker_id_dict.keys())
        yql_query = yql_query + ticker_url + "')"
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + \
                  "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
        # get data
        for i in range(5):
            try:
                result = urllib2.urlopen(yql_url).read()
                log_string = '(QUERY:' + yql_url + '),SUCCESS'
                logger.info(log_string)
                break
            except:
                log_string = '(QUERY:' + yql_url + '),FAIL'
                logger.info(log_string)
                if (i == 4):
                    return
        data = json.loads(result)
        quote_data = data['query']['results']['quote']

        # create objects
        quotes = [Entry.Quote(id=ticker_id_dict[q['symbol']],
                               price=unicode2int(q['LastTradePriceOnly']),
                               volume=q['Volume'],
                               time=fetch_time)
                  for q in quote_data]
        count = len(quotes)
        # write results into db
        Entry.Quote.add(quotes)
        result = 'True'
    except Exception as e:
        result = 'False'
        logger_alert.exception('fetch_error@' + str(fetch_time))

    finish_time = datetime.datetime.now()
    log_string = "[({0}),({1}),{2},{3}]".format(start_time, finish_time, result, count)
    logger.info(log_string)


def run():
    ticker_dict = get_stock_list()
    fetch_quotes(ticker_dict)
