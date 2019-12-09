from stock_report.abstract import base
from pprint import pprint

'''
twse_daily_transaction_adapater
'''
class adapter(base):
    def __init__(self):
        ''' constructor '''

    def transform(self, row, *args, **kwargs):
        '''
        :param row:
        :param args:
        :param kwargs:
        :return: dict
        '''
        if type(row) is list:
            return self._transform_from_list(row)
        else:
            return self._transform_from_string(row)

    def _transform_from_list(self, row, *args, **kwargs):
        '''
        transform TWSE daily transaction information from list to dictionary

        :param row: TWSE daily transaction information list
        :param args:
        :param kwargs:
        :return: dict
        '''
        return {
            'date': row[0],  # 日期
            'volume': row[1],  # 成交股數/ 成交量
            'amount_of_transaction': row[2],  # 成交金額,
            'open': row[3],  # 開盤價
            'high': row[4],  # 最高價
            'low': row[5],  # 最低價
            'close': row[6],  # 收盤價
            'spread': row[7],  # 價差
            'number_of_transactions': row[8]  # 成交筆數
        }

    def _transform_from_string(self, row, *args, **kwargs):
        '''
        transform TWSE daily transaction information from string to dictionary

        :param row: TWSE daily transaction information string
        :param args:
        :param kwargs:
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
