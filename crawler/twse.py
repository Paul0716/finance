#!/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from functools import reduce
from pprint import pprint

import requests

from abstract.base import base
from stock_report.utils import *

time_interval = 3


class crawler(base):
    def __init__(self, stock_number, *args, **kwargs):
        self.stock_number = stock_number
        self.repository = kwargs['repository'] if 'repository' in kwargs.keys() else None
        self.adapter = kwargs['adapter'] if 'adapter' in kwargs.keys() else None
        super(base, self)

    def execute(self, *args, **kwargs):
        stock_number = self.stock_number
        start = kwargs['start']
        end = kwargs['end']
        walker = kwargs['walker'] if 'walker' in kwargs.keys() else None
        result = []
        twse_date_list = []

        existing_date_list = list(
            map(lambda row: self._convert_tw_datetime(row[0]), self.repository.read(name=stock_number)))
        existing = reduce(self._check_datetime_exists, existing_date_list, {
            'last': None,
            'date': [],
        })
        pprint(existing)
        tmp_date = start
        while tmp_date <= end:
            date_param = tmp_date.strftime('%Y%m01')
            if date_param not in existing['date'] and date_param not in twse_date_list:
                twse_date_list.append(date_param)
            # add a day to tmp_date
            tmp_date = tmp_date + datetime.timedelta(days=1)

        # loop for every date string
        for date_str in twse_date_list:
            url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date_str}&stockNo={stock_number}'
            response = requests.get(url, allow_redirects=True)
            log = f'status code: {response.status_code} , url: {url}'
            print(log)
            if response.status_code is 200:

                content = response.content.decode('cp1252')
                for row in content.split('\r\n')[2:22]:

                    if len(row.split('","')) < 9:
                        continue

                    if walker is not None:
                        dict = walker(row=row)
                    else:
                        raise IOError('walker should not be None')

                    result.append(dict)
                self.complete(data=result)
                time.sleep(time_interval)

            else:
                log = f"發生錯誤: status_code: {response.status_code}, date: {date_param}, url: {response.url.encode('utf-8')} "
                self._record_error_log(log=log)

    def complete(self, *args, **kwargs):
        self.repository.save(name=self.stock_number, data=kwargs['data'])

    def _record_error_log(self, *args, **kwargs):
        line = kwargs['log'] + '\n'
        error_log = open('error.log', 'ab')
        error_log.write(line.encode())
        error_log.close()

    def _convert_tw_datetime(self, date_str):
        if date_str is not None:
            date_list = date_str.split('/')
            return '/'.join([
                str(int(date_list[0]) + 1911),
                date_list[1],
                date_list[2]
            ])
        else:
            raise IOError('date_str parameters are required.')

    def _check_datetime_exists(self, accumaltor, date_str):
        date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
        if accumaltor['last'] is None or accumaltor['last'] < date:
            accumaltor['last'] = date
        exists = date.strftime('%Y%m01') in accumaltor['date']
        if not exists:
            accumaltor['date'].append(date.strftime('%Y%m01'))

        return accumaltor
