"""
Transaction module
"""

import datetime

from src.DB.Models import *
from src.fetch_data import chop_microseconds


class order_control(object):
    """docstring for order_control"""

    def __init__(self):
        pass

    def buy(self, portfolio, stock, shares, price):
        # get order time
        start_time = datetime.datetime.now()
        order_time = chop_microseconds(start_time)
        # do calculation
        commission = 700
        total = price * shares - commission
        # get portfolio and stock id
        port = Portfolio.search(name=portfolio)
        stock = Stock.search(name=stock)
        # record transaction
        trans = Transaction(time=order_time, portfolio=port['id'],
                            stock=stock, action='buy', shares=shares,
                            price=price, total=total)
        Transaction.add([trans])
        # record change in position
        pos = Position.search(portfolio=portfolio, stock=stock)
        if pos is None:
            pos = Position(portfolio=portfolio, stock=stock, shares=shares,
                           avg_cost=total / shares, total_cost=total)
            Position.add([pos])
        elif isinstance(pos[0], Position):
            pos['shares'] += shares
            pos['total_cost'] += total
            pos['avg_cost'] = pos['total_cost'] / pos['shares']
            pos.save()

    def order(self, portfolio, stock, action, shares, price):
        start_time = datetime.datetime.now()
        order_time = chop_microseconds(start_time)

        if action == 'buy':
            commission = 700
            total = price * shares - commission
            transaction = Transaction(time=order_time, portfolio=portfolio,
                                      stock=stock, action=buy, shares=shares,
                                      price=price, total=total)
            pos = Position.search(portfolio=portfolio, stock=stock)
            if pos is None:
                pos = Position(portfolio=portfolio, stock=stock, shares=shares, avg_cost=total / shares,
                               total_cost=total)
                Position.add([pos])
            elif isinstance(pos[0], Position):
                pos['shares'] += shares
                pos['total_cost'] += total
                pos['avg_cost'] = pos['total_cost'] / pos['shares']
                pos.save()

        elif action == 'sell':
            pass
        elif action == 'short':
            pass
        elif action == 'btc':
            pass


if __name__ == '__main__':
    a = order_control()
    a.buy(portfolio='MACD', )
