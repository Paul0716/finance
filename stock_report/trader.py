from stock_report.abstract import base
from pprint import pprint

class trader(base):

    ''' in stock '''
    amount = 0

    ''' cash '''
    cash = 1000000

    def __init__(self, stock_number, *args, **kwargs):
        self.stock_number = stock_number

        self.stock_items = kwargs['stock_items'] if 'stock_items' in kwargs.keys() else None
        self.cash = kwargs['cash'] if 'cash' in kwargs.keys() else None

        super(base, self)

    def sell(self, *args, **kwargs):
        # sell method
        amount = kwargs['amount']
        price = kwargs['price']
        amount_of_transaction = self._get_amount_of_transaction(amount=amount, price=price)
        valid = self.amount > 0

        self.cash = (self.cash + amount_of_transaction) if valid else self.cash
        self.amount = self.amount - amount if valid else self.amount

        kwargs.update({
            'stock_number': self.stock_number,
            'cash': self.cash,
            'stock_amount': self.amount
        })
        self.log(log='[%(stock_number)s] sell amount: %(amount)d, price: %(price)s, cash: %(cash)s, stock_amount: %(stock_amount)s' % kwargs)

    def buy(self, *args, **kwargs):
        # sell method
        amount = kwargs['amount']
        price = kwargs['price']
        amount_of_transaction = self._get_amount_of_transaction(amount=amount, price=price)
        valid = self.cash > amount_of_transaction

        self.cash = (self.cash - amount_of_transaction) if valid else self.cash
        self.amount = self.amount + amount if valid else self.amount

        kwargs.update({
            'stock_number': self.stock_number,
            'cash': self.cash,
            'stock_amount': self.amount
        })
        self.log(log='[%(stock_number)s] buy amount: %(amount)d, price: %(price)s, cash: %(cash)s, stock_amount: %(stock_amount)s' % kwargs)


    def should_stop_profit(self, *args, **kwargs):
        # stop profit method
        # self.log(log='stop profit: %s, price: %s' % ( kwargs['amount'], kwargs['price']))
        return False

    def should_stop_loss(self, *args, **kwargs):
        # stop loss method
        # self.log(log='stop loss: %s, price: %s' % (kwargs['amount'], kwargs['price']))
        return False

    def log(self, *args, **kwargs):
        # log method
        log = kwargs['log']
        pprint(log)

    def _get_amount_of_transaction(self, *args, **kwargs):
        return kwargs['amount'] * float(kwargs['price']) * 1000