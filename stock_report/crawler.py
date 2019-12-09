#!/bin/python
# -*- coding: utf-8 -*-

from .utils import *
from pprint import pprint
from stock_report.abstract import base

class crawler(base):
    def __init__(self, stock_number):
        self.stock_number = stock_number
        super(base, self)


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
                        'stringValue': row['amount_of_transaction']
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

        if len(sheet_prop) == 0:
            response = self.sheet_client.addSheet(spreadsheetId=sheet['id'], body={
                'properties': {
                    'index': 0,
                    'title': tab_title,
                    'gridProperties': {
                        'rowCount': len(kwargs['data']),
                        'columnCount': 9
                    }
                },
            })
            sheet_prop = list(map(lambda response: response['addSheet'],response['replies']))

        sheet_data = self.sheet_client.read(
            spreadsheetId=sheet['id'],
            ranges=self.get_grids_rangs(
                columnCount=sheet_prop[0]['properties']['gridProperties']['columnCount'],
                rowCount=sheet_prop[0]['properties']['gridProperties']['rowCount']
            ),
            valueRenderOption='UNFORMATTED_VALUE',
            dateTimeRenderOption='FORMATTED_STRING'
        )
        existing_data = self.get_daily_data(data=sheet_data)
        existing_date_list = list(map(lambda row: row[0], existing_data)) if existing_data is not None else []

        append_data = list(filter(lambda row: row['date'] not in existing_date_list, kwargs['data']))
        append_data = list(map(self._daily_twse_mapper, append_data))

        if len(append_data) > 0:
            self.sheet_client.appendCells(spreadsheetId=sheet['id'], body={
                'sheetId': sheet_prop[0]['properties']['sheetId'],
                'fields': '*',
                'rows': append_data
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
