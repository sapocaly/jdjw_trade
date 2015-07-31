# coding=utf-8

"""
Transaction module
"""

import datetime

from src.DB.Models import *
from src.utils.DbUtils import chop_microseconds
import utils.LogConstant as LogConstant


class OrderControl(object):
    """OrderControl module"""

    commission = 700
    logger = LogConstant.ORDER_DIGEST_LOGGER
    logger_alert = LogConstant.ORDER_DIGEST_LOGGER_ALERT

    def __init__(self):
        pass

    def buy(self, portfolio, stock, shares, price):
        # get order time
        start_time = datetime.datetime.now()
        order_time = chop_microseconds(start_time)
        try:
            # do calculation
            total = price * shares + self.commission
            # get portfolio, cash position, and stock id
            port = Portfolio.search(name=portfolio)[0]
            st = Stock.search(ticker=stock)[0]
            cash = Position.search(portfolio=port['id'], stock=0)[0]
            if cash['total_cost'] < total:
                result = 'False'
                self.logger_alert.exception('Order_error: buy@' + str(order_time) + ': portfolio %s not enough balance' % portfolio)
            else:
                # add or update position
                positions = Position.search(portfolio=port['id'], stock=st['id'])
                if positions == []:
                    pos = Position(portfolio=port['id'], stock=st['id'], shares=shares,
                                       avg_cost=total / shares, total_cost=total, aggr_cost=total)
                    Position.add([pos])
                else:
                    pos = positions[0]
                    pos['shares'] += shares
                    pos['total_cost'] += total
                    pos['aggr_cost'] += total
                    pos['avg_cost'] = pos['total_cost'] / pos['shares']
                    pos.save()
                # update cash
                cash['shares'] -= total
                cash['total_cost'] -= total
                cash.save()
                # record transaction
                trans = Transaction(time=order_time, portfolio=port['id'],
                                    stock=st['id'], action='buy', shares=shares,
                                    price=price, total=total)
                Transaction.add([trans])
                result = 'True'
        except Exception:
            result = 'False'
            self.logger_alert.exception('Order_error: buy@' + str(order_time))
        log_string = '%s: portfolio %s bought %d shares %s @ $%d/share. %s.' % (str(order_time), portfolio, shares, stock, price, result)
        self.logger.info(log_string)

    def sell(self, portfolio, stock, shares, price):
        # get order time
        start_time = datetime.datetime.now()
        order_time = chop_microseconds(start_time)
        try:
            # do calculation
            total = price * shares - self.commission
            # get portfolio, position, cash, and stock id
            port = Portfolio.search(name=portfolio)[0]
            st = Stock.search(ticker=stock)[0]
            cash = Position.search(portfolio=port['id'], stock=0)[0]
            pos = Position.search(portfolio=port['id'], stock=st['id'])[0]
            if pos['shares'] < shares:
                result = 'False'
                self.logger_alert.exception('Order_error: sell@' + str(order_time) + ': portfolio %s not enough shares' % portfolio)
            else:
                # update position
                pos['total_cost'] -= pos['total_cost'] * shares / pos['shares']
                pos['shares'] -= shares
                pos['aggr_cost'] -= total
                if pos['shares'] == 0:
                    pos['avg_cost'] = 0
                pos.save()
                # update cash
                cash['shares'] += total
                cash['total_cost'] += total
                cash.save()
                # record transaction
                trans = Transaction(time=order_time, portfolio=port['id'],
                                    stock=st['id'], action='sell', shares=(-shares),
                                    price=price, total=(-total))
                Transaction.add([trans])
            result = 'True'
        except Exception:
            result = 'False'
            self.logger_alert.exception('Order_error: sell@' + str(order_time))
        log_string = '%s: portfolio %s sold %d shares %s @ $%d/share. %s.' % (str(order_time), portfolio, shares, stock, price, result)
        self.logger.info(log_string)
    
    def short(self, portfolio, stock, shares, price):
        # get order time
        start_time = datetime.datetime.now()
        order_time = chop_microseconds(start_time)
        try:
            # do calculation
            total = price * shares - self.commission
            # get portfolio, cash, and stock id
            port = Portfolio.search(name=portfolio)[0]
            st = Stock.search(ticker=stock)[0]
            cash = Position.search(portfolio=port['id'], stock=0)[0]
            # add or update position
            result = Position.search(portfolio=port['id'], stock=st['id'])
            if result == []:
                pos = Position(portfolio=port['id'], stock=st['id'], shares=(-shares),
                                   avg_cost=total / shares, total_cost=(-total), aggr_cost=(-total))
                Position.add([pos])
            else:
                pos = result[0]
                if pos['shares'] > 0:
                    result = 'False'
                    self.logger_alert.exception('Order_error: short@' + str(order_time) + ': portfolio %s has long position' % portfolio)
                else:
                    pos['shares'] -= shares
                    pos['total_cost'] -= total
                    pos['avg_cost'] = pos['total_cost'] / pos['shares']
                    pos['aggr_cost'] -= total
                    pos.save()
            # update cash
            cash['shares'] += total
            cash['total_cost'] += total
            cash.save()
            # record transaction
            trans = Transaction(time=order_time, portfolio=port['id'],
                            stock=st['id'], action='short', shares=(-shares),
                            price=price, total=(-total))
            Transaction.add([trans])
            result = 'True'
        except Exception:
            result = 'False'
            self.logger_alert.exception('Order_error: short@' + str(order_time))
        log_string = '%s: portfolio %s shortsold %d shares %s @ $%d/share. %s.' % (str(order_time), portfolio, shares, stock, price, result)
        self.logger.info(log_string)

    def btc(self, portfolio, stock, shares, price):
        # get order time
        start_time = datetime.datetime.now()
        order_time = chop_microseconds(start_time)
        try:
            # do calculation
            total = price * shares + self.commission
            # get portfolio, cash, and stock id
            port = Portfolio.search(name=portfolio)[0]
            st = Stock.search(ticker=stock)[0]
            cash = Position.search(portfolio=port['id'], stock=0)[0]
            pos = Position.search(portfolio=port['id'], stock=st['id'])[0]
            # add or update position
            if pos['shares'] > -shares:
                result = 'False'
                self.logger_alert.exception('Order_error: btc@' + str(order_time) + ': portfolio %s not enough short position' % portfolio)
            else:
                pos['total_cost'] += pos['total_cost'] * shares / pos['shares']
                pos['shares'] += shares
                if pos['shares'] == 0:
                    pos['avg_cost'] = 0
                pos['aggr_cost'] += total
                pos.save()
            # update cash
            cash['shares'] -= total
            cash['total_cost'] -= total
            cash.save()
            # record transaction
            trans = Transaction(time=order_time, portfolio=port['id'],
                            stock=st['id'], action='btc', shares=shares,
                            price=price, total=total)
            Transaction.add([trans])
            result = 'True'
        except Exception:
            result = 'False'
            self.logger_alert.exception('Order_error: btc@' + str(order_time))
        log_string = '%s: portfolio %s bought to cover %d shares %s @ $%d/share. %s.' % (str(order_time), portfolio, shares, stock, price, result)
        self.logger.info(log_string)


if __name__ == '__main__':
    a = OrderControl()
    #a.btc('MACD', 'YHOO', 300, 4000)
    #a.sell('MACD', 'YHOO', 300, 4000)
