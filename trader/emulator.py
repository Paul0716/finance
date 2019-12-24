from functools import reduce
from math import floor
from pprint import pprint

from abstract.base import base
from trader.trade_type import TradeType, Action


class emulator(base):
    # in stock
    amount = 0
    # trade history
    history = []
    # cash
    cash = 1000000

    def __init__(self, stock_number, *args, **kwargs):
        self.stock_number = stock_number

        self.stock_items = kwargs['stock_items'] if 'stock_items' in kwargs.keys() else None
        self.cash = kwargs['cash'] if 'cash' in kwargs.keys() else None

        super(base, self)

    def sell(self, *args, **kwargs):
        # sell method
        amount = self._get_trade_amount(type=TradeType.All)
        price = float(kwargs['price'])
        date = kwargs['date']
        amount_of_transaction = self._get_amount_of_transaction(amount=amount, price=price)
        valid = self.amount > 0
        self.cash = (self.cash + amount_of_transaction) if valid else self.cash
        self.amount = self.amount - amount if valid else self.amount

        if valid:
            self.history.append({
                'date': date,
                'amount': amount,
                'price': price,
                'cash': self.cash,
                'action': Action.Sell
            })
            message = f'[{date}][{self.stock_number}] sell amount: {amount}, price: {price}, cash: {self.cash}, stock_amount: {self.amount}'
            self.log(
                log=message)

    def buy(self, *args, **kwargs):
        # buy method
        price = float(kwargs['price'])
        amount = floor(self._get_trade_cash(type=kwargs['type']) / price)
        date = kwargs['date']
        amount_of_transaction = self._get_amount_of_transaction(amount=amount, price=price)
        valid = self.cash > amount_of_transaction

        self.cash = (self.cash - amount_of_transaction) if valid else self.cash
        self.amount = self.amount + amount if valid else self.amount
        if valid and amount > 0:
            self.history.append({
                'date': date,
                'amount': amount,
                'price': price,
                'cash': self.cash,
                'action': Action.Buy
            })
            message = f'[{date}][{self.stock_number}] buy amount: {amount}, price: {price}, cash: {self.cash}, stock_amount: {self.amount}'
            self.log(
                log=message)

    def should_stop_profit(self, *args, **kwargs):
        # stop profit method
        # self.log(log='stop profit: %s, price: %s' % ( kwargs['amount'], kwargs['price']))
        return False

    def should_stop_loss(self, *args, **kwargs):
        # stop loss method
        # self.log(log='stop loss: %s, price: %s' % (kwargs['amount'], kwargs['price']))
        return False

    def performance_report(self):
        def _calculate_profit(accumerlator, trade):
            return accumerlator - floor(trade['amount'] * float(trade['price'])) if trade[
                                                                                        'action'] is Action.Buy else accumerlator + floor(
                trade['amount'] * float(trade['price']))

        performance = reduce(_calculate_profit, self.history, 0)
        message = f'profit: {performance}'
        pprint(message)
        return {
            'performance': performance,
        }

    def log(self, *args, **kwargs):
        # log method
        log = kwargs['log']
        pprint(log)

    def _get_amount_of_transaction(self, *args, **kwargs):
        return floor(kwargs['amount'] * kwargs['price'])

    def _get_trade_amount(self, *args, **kwargs):
        type = kwargs['type']
        if type is TradeType.All:
            return self.amount
        elif type is TradeType.Half:
            return floor(self.amount * 0.5)
        else:
            return 0

    def _get_trade_cash(self, *args, **kwargs):
        type = kwargs['type']
        if type is TradeType.All:
            return self.cash
        elif type is TradeType.Half:
            return floor(self.cash * 0.5)
        else:
            return 0
