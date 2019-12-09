from stock_report.abstract import base
from pprint import pprint

class trader(base):
    ''' in stock '''
    stock_items = []

    ''' cash '''
    cash = 0

    def __init__(self, stock_number, *args, **kwargs):
        self.stock_number = stock_number

        self.stock_item = kwargs['stock_items'] if 'stock_items' in kwargs.keys() else None
        self.cash = kwargs['cash'] if 'cash' in kwargs.keys() else None

        super(base, self)

    def sell(self, *args, **kwargs):
        ''' sell method '''
        self.log(log='buy amount: %s, price: %s' % (kwargs['amount'], kwargs['price']))

    def buy(self, *args, **kwargs):
        ''' buy method '''
        self.log(log='buy amount: %s, price: %s' % ( kwargs['amount'], kwargs['price'] ))

    def should_stop_profit(self, *args, **kwargs):
        ''' stop profit method '''

    def should_stop_loss(self, *args, **kwargs):
        ''' stop loss method '''

    def log(self, *args, **kwargs):
        ''' log method '''
