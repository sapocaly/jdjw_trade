import urllib2
import urllib
import json
import datetime

from src.DB.Models import *
from src.DB.DAL import StockDAL
from src.utils.DbUtils import unicode2int


# todo: update
def rm_after_market_quotes():
    ## US East
    # sql = 'SELECT * from quote where ' +\
    #    'weekday(time) > 4 or ' +\
    #    'extract(hour_second from time) > 160000 or ' +\
    #    'extract(hour_second from time) < 93000'
    dal_instance = StockDAL()
    sql = 'SELECT * from quote where ' + \
          '(weekday(time) = 0 and extract(hour_second from time) < 40001) or ' + \
          '(weekday(time) = 5 and extract(hour_second from time) > 212959) or ' + \
          'weekday(time) = 6 or ' + \
          '(extract(hour_second from time) > 40000 and ' + \
          'extract(hour_second from time) < 213000)'
    records = dal_instance.select(sql)
    after_market_quotes = [Quote(id=quo[0], price=quo[1], volume=quo[2], time=quo[3]) for quo in records]
    if after_market_quotes != []:
        print 'After market quotes retrieved. Removing...'
    Quote.rm(after_market_quotes)


def update_company_info():
    stocks = Stock.search()
    tickers = [x['ticker'] for x in stocks]
    # get company info and stores in db
    # build query url for api
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from yahoo.finance.quote where symbol in ('"
    ticker_url = "','".join(tickers)
    yql_query = yql_query + ticker_url + "')"
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + \
              "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
    print yql_url
    # get data
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    quote_data = data['query']['results']['quote']
    for q in quote_data:
        stock = Stock.search(ticker=q['symbol'])[0]
        stock['name'] = q['Name'][:20]
        stock['exchange'] = q['StockExchange']
        stock['pv_close'] = unicode2int(q['LastTradePriceOnly'])
        stock['pv_volume'] = q['Volume']
        stock.save()


def check_data_integrity():
    dal_instance = StockDAL()
    stocks = dal_instance.select('select count(*) from stock')[0][0]
    timestamps = dal_instance.select('select count(*), time from quote group by time order by time')
    print "Total: %d distinct timestamps, should have %d stocks." % (len(timestamps), stocks)
    incomplete_count = 0
    for stamp in timestamps:
        if stamp[0] != stocks:
            incomplete_count += 1
            print 'Incomplete quote %d at %s: %d stocks' % (incomplete_count, stamp[1], stamp[0])
    time_skip = 0
    for i in range(1, len(timestamps)):
        if timestamps[i][1] - timestamps[i - 1][1] != datetime.timedelta(0, 1):
            time_skip += 1
            print 'Time skip %s: (%s)' % (time_skip, timestamps[i][1] - timestamps[i - 1][1])
            print timestamps[i - 1][1]
            print timestamps[i][1]


def solve_time_skip():
    """
    this assumes that there is no after market data
    """
    dal_instance = StockDAL()
    timestamps = dal_instance.select('select count(*), time from quote group by time order by time')
    # solve time skip
    for i in xrange(1, len(timestamps)):
        if timestamps[i][1] - timestamps[i - 1][1] != datetime.timedelta(0, 1):
            if timestamps[i][1] - timestamps[i - 1][1] < datetime.timedelta(0, 60):
                duration = (timestamps[i][1] - timestamps[i - 1][1]).seconds
                for st in Stock.search():
                    id = st['id']
                    beg_quote = Quote.search(id=id, time=timestamps[i - 1][1])[0]
                    end_quote = Quote.search(id=id, time=timestamps[i][1])[0]
                    beg_price = beg_quote['price']
                    end_price = end_quote['price']
                    beg_vlm = beg_quote['volume']
                    end_vlm = end_quote['volume']
                    for t in xrange(1, duration):
                        time = timestamps[i - 1][1] + datetime.timedelta(0, t)
                        print time
                        price = beg_price + (end_price - beg_price) / duration * t
                        volume = beg_vlm + (end_vlm - beg_vlm) / duration * t
                        quote = Quote(id=id, time=time, price=price, volume=volume)
                        Quote.add([quote])
                        print 'Added quote for %s at %s and at $%s, vlm %s' % (st['ticker'], time, price, volume)


def solve_incomplete_stock():
    """
    this assumes that there is no time skip
    """
    dal_instance = StockDAL()
    stocks = Stock.search()
    timestamps = dal_instance.select('select count(*), time from quote group by time order by time')
    for i in xrange(1, len(timestamps) - 1):
        if timestamps[i][0] != len(stocks):
            time = timestamps[i][1]
            stocks_recorded = [quote['id'] for quote in Quote.search(time=time)]
            stocks_complete = [st['id'] for st in Stock.search()]
            for id in stocks_complete:
                if id not in stocks_recorded:
                    beg_quote = Quote.search(id=id, time=timestamps[i - 1][1])[0]
                    end_quote = Quote.search(id=id, time=timestamps[i + 1][1])[0]
                    price = (beg_quote['price'] + end_quote['price']) / 2
                    volume = (beg_quote['volume'] + end_quote['volume']) / 2
                    quote = Quote(id=id, time=time, price=price, volume=volume)
                    Quote.add([quote])
                    print 'Added quote for stock ID:%s at %s and at $%s, vlm %s' % (id, time, price, volume)


if __name__ == '__main__':
    rm_after_market_quotes()
    # update_company_info()
    # check_data_integrity()
    # solve_time_skip()
    # solve_incomplete_stock()
