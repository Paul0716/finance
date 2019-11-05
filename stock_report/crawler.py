#!/bin/python
# -*- coding: utf-8 -*-

from .utils import *
from pprint import pprint
from google_client.sheets import google_sheets
from google_client.drive import google_drive

class crawler:
    def __init__(self, stock_number):
        self.stock_number = '0050'
        self.target_folder = 'Taiwan Index Stock'

        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        # google sheet client
        self.sheet_client = google_sheets(scope, path='./client_secret.json')
        # google drive client
        self.drive_client = google_drive(scope, path='./client_secret.json')


    def twse_daily_transaction_adapter(self, row):
        '''
        :param row: TWSE daily transaction information string
        :return: dict
        '''
        def remove_doulbe_quote(string):
            return string.replace('"', '')

        def remove_comma(string):
            return ''.join(string.split(','))

        list = row.split('","')
        for (index, value) in enumerate(list):
            list[index] = remove_comma(remove_doulbe_quote(value))

        return {
            'date': remove_doulbe_quote(list[0]),  # 日期
            'volume': remove_comma(list[1]),  # 成交股數/ 成交量
            'amount_of_transaction': remove_comma(list[2]),  # 成交金額,
            'open': remove_comma(list[3]),  # 開盤價
            'high': remove_comma(list[4]),  # 最高價
            'low': remove_comma(list[5]),  # 最低價
            'close': remove_comma(list[6]),  # 收盤價
            'spread': remove_comma(list[7]),  # 價差
            'number_of_transactions': remove_comma(list[8])  # 成交筆數
        }

    def _get_target_sheet(self):
        return self.drive_client.find_target_sheet(self.stock_number)

    def _get_target_folder(self):
        return self.drive_client.get_root_folder(self.target_folder)

    def _daily_twse_mapper(self, row):
        return {
            'values': [
                {
                    'userEnteredValue': {
                        'stringValue': row['date']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['volume']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['open']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['high']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['low']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['close']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['spread']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['number_of_transactions']
                    }
                },
            ]
        }

    def _batch_update_google_sheet(self, *args, **kwargs):
        tab_title = 'Daily'
        folder = self._get_target_folder()
        sheet = self._get_target_sheet()
        if sheet is None:
            sheet = self.drive_client.add_new_sheet(name=self.stock_number, parent=folder)

        # get target via google sheet API
        target = self.sheet_client.get(spreadsheetId=sheet['id'])
        sheet_prop = self.sheet_client.find_sheet_by_name(spreadsheet_properties=target, sheet_name=tab_title)
        pprint(target)
        if len(sheet_prop) == 0:
            sheet_prop = self.sheet_client.addSheet(spreadsheetId=sheet['id'], body={
                'properties': {
                    'index': 0,
                    'title': tab_title,
                    'gridProperties': {
                        'rowCount': len(kwargs['data']),
                        'columnCount': 9
                    }
                },
            })
        pprint(sheet_prop)
        append_data = map(self._daily_twse_mapper, kwargs['data'])
        self.sheet_client.appendCells(spreadsheetId=sheet['id'], body={
            'sheetId': sheet_prop[0]['properties']['sheetId'],
            'fields': '*',
            'rows': list(append_data)
        })


    def execute(self, *args, **kwargs):
        get_single_page(stock_number=self.stock_number,
                        start=kwargs['start'],
                        end=kwargs['end'],
                        adapter=self.adapter,
                        complete=self.complete)

    def adapter(self, *args, **kwargs):
        return self.twse_daily_transaction_adapter(row=kwargs['row'])

    def complete(self, *args, **kwargs):
        return self._batch_update_google_sheet(data=kwargs['data'])
