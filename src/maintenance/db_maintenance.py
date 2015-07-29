import urllib2
import urllib
import json
import datetime

from src.DB import Models
from src.DB.DAL import StockDAL
from src.utils.DbUtils import unicode2int


def rm_after_market_quotes():
    ## US East
    # if (time.weekday() > 4) or\
    #        ((time.hour > 4 or (time.hour == 4 and time.minute > 0))and
    #         (time.hour < 21 or (time.hour == 21 and time.minute < 30))):
    after_market_quotes = []
    for quote in Models.Quote.search():
        time = quote['time']
        # GMT +8
        if (time.weekday() == 0 and (time.hour < 4 or (time.hour == 4 and time.minute == 0))) or \
                (time.weekday() == 5 and (time.hour > 21 or (time.hour == 21 and time.minute >= 30))) or \
                        time.weekday() == 6 or \
                ((time.hour > 4 or (time.hour == 4 and time.minute > 0)) and
                     (time.hour < 21 or (time.hour == 21 and time.minute < 30))):
            after_market_quotes.append(quote)
    Models.Quote.rm(after_market_quotes)


def update_company_info():
    stocks = Models.Stock.search()
    tickers = [x['ticker'] for x in stocks]
    # get company info and stores in db
    # build query url for api
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from yahoo.finance.quote where symbol in ('"
    ticker_url = "','".join(tickers)
    yql_query = yql_query + ticker_url + "')"
    yql_url = baseurl + urllib.urlencode({'q': yql_query}) + \
              "&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys&callback="
    # print yql_url
    # get data
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    quote_data = data['query']['results']['quote']
    for q in quote_data:
        stock = Models.Stock.search(ticker=q['symbol'])[0]
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


if __name__ == '__main__':
    # rm_after_market_quotes()
    update_company_info()
    check_data_integrity()
