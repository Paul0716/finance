#!/bin/python
# -*- coding: utf-8 -*-

import datetime
from .utils import *
from pprint import pprint

class crawler:

    target = 'tsec'

    def __init__(self, source):
        '''

        :param source: crawler url string
        '''
        self.source = source;

    def execute(self):
        print('execut')
        stock_list = ['0050']
        # stock_list = get_stock_list()
        today = datetime.datetime.today()
        index = 0

        while index < len(stock_list):
            stock_id = stock_list[index]
            stock_date = today - datetime.timedelta(days=4 * 365)
            index += 1
            while not (today.year == stock_date.year and stock_date.month > today.month):
                pprint(stock_id, stock_date.year, stock_date.month)
                pprint(stock_id, today.year, today.month)
                stock_date = date_add_a_month(stock_date)
                get_single_page(stock_id, str(stock_date.year), str(stock_date.month).zfill(2))
