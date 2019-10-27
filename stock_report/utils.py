#!/bin/python
# -*- coding: utf-8 -*-

import csv
import requests
import os
from pyquery import PyQuery as pq

def get_single_page(stock_id, year, month):
    path = 'data/%s.csv' % stock_id

    check_if_file_exists(path)

    csv_data = read_single_file(path)

    with open(path, 'ab') as f:
        cw = csv.writer(f)
        page = requests.get(
            'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report' + year + month + '/' + year + month + '_F3_1_8_' + stock_id + '.php?STK_NO=' + stock_id + '&myear=' + year + '&mmon=' + month)
        if page.status_code is 200:
            d = pq(page.text)
            row = d('tr.basic2')
            for key, value in enumerate(row):
                if key is not 0:
                    data = d(value).text().strip('"').split(' ')

                    if data not in csv_data:
                        cw.writerow(data)
            f.close();
        else:
            record_error_log("發生錯誤: status_code: %(code)s, year: %(year)s, month: %(month)s, url: %(url)s " % {
                'code': page.status_code, 'year': year, 'month': month, 'url': page.url.encode('utf-8')})


def get_stock_list(filename):

    stock_id_list = []
    f = open(filename, 'rb')
    for row in csv.reader(f, delimiter=','):
        stock_id_list.append(row[0])
    return stock_id_list


# 錯誤輸出檔案
def record_error_log(msg):
    error_log = open('error.log', 'ab')
    error_log.write(msg + '/r/n')
    error_log.close()
    return msg


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

