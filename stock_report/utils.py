#!/bin/python
# -*- coding: utf-8 -*-

import csv
import datetime


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


def tw_time_converter(*args, **kwargs):
    target_date = args[0]
    year = int(target_date[0])
    month = int(target_date[1])
    day = int(target_date[2])
    return datetime.date(year + 1911, month, day + 1).strftime("%Y-%m-%d")


def date_add_a_month(obj):
    if obj.month < 12:
        mon = obj.month + 1
        return obj.replace(month=mon)
    else:
        year = obj.year + 1
        mon = 1
        return obj.replace(year=year, month=mon)
