#!/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime
import os
import requests
from pprint import pprint

def get_single_page(*args, **kwargs):
    stock_number = kwargs['stock_number']
    start = kwargs['start']
    end = kwargs['end']
    walker = kwargs['walker'] if 'walker' in kwargs.keys() else None
    adapter = kwargs['adapter'] if 'adapter' in kwargs.keys() else None
    complete = kwargs['complete'] if 'complete' in kwargs.keys() else None

    result = []
    twse_date_list = []

    tmp_date = start
    while tmp_date <= end:
        date_param = tmp_date.strftime('%Y%m01')
        if date_param not in twse_date_list:
            twse_date_list.append(date_param)
        # add a day to tmp_date
        tmp_date = tmp_date + datetime.timedelta(days=1)


    # loop for every date string
    for date_str in twse_date_list:
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date=%(date)s&stockNo=%(stock_number)s" % {
            "stock_number": stock_number,
            "date": date_str
        }
        response = requests.get(url, allow_redirects=True)

        if response.status_code is 200:
            content = response.content.decode('cp1252')
            for row in content.split('\r\n')[2:22]:
                dict = adapter(row=row, stock_number=stock_number)

                if walker is not None:
                    walker(dict)

                result.append(dict)

            # complete
            if complete is not None:
                complete(data=result, stock_number=stock_number)


        else:
            record_error_log("發生錯誤: status_code: %(code)s, date_param: %(date)s url: %(url)s " % {
                'code': response.status_code, 'date': date_param, 'url': response.url.encode('utf-8')})



def get_stock_list(filename):

    stock_id_list = []
    f = open(filename, 'rb')
    for row in csv.reader(f, delimiter=','):
        stock_id_list.append(row[0])
    return stock_id_list


# 錯誤輸出檔案
def record_error_log(msg):
    line = msg + '\n'
    error_log = open('error.log', 'ab')
    error_log.write(line.encode())
    error_log.close()

# 讀取檔案
def read_single_file(csvfile):
    data_list = []
    with open(csvfile, 'r') as f:
        x = csv.reader(f, delimiter=',', quotechar='"')
        for row in x:
            data_list.append(row)
        return data_list


def tw_time_converter(*args, **kwargs):
    target_date = args[0]
    year = int(target_date[0])
    month = int(target_date[1])
    day = int(target_date[2])
    return datetime.date(year + 1911, month, day + 1).strftime("%Y-%m-%d")


def overwrite_csv_line(*args, **kwargs):
    with open(kwargs['csvfile'], 'w') as b:
        writer = csv.writer(b)
        print
        kwargs["data"]
        writer.writerow(kwargs["data"])


def date_add_a_month(obj):
    if obj.month < 12:
        mon = obj.month + 1
        return obj.replace(month=mon)
    else:
        year = obj.year + 1
        mon = 1
        return obj.replace(year=year, month=mon)


def check_if_file_exists(filename):
    if not os.path.isfile(filename):
        open(filename, 'a').close()
        print
        "create file %s" % filename

