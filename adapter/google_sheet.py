import re
from os import path
from google_client.drive import google_drive
from google_client.sheets import google_sheets

class adapter:
    target_folder = 'Taiwan Index Stock'
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    sheet_client = google_sheets(scope, path=path.abspath('../client_secret.json'))
    drive_client = google_drive(scope, path=path.abspath('../client_secret.json'))

    def _get_target_sheet(self, *args, **kwargs):
        return self.drive_client.find_target_sheet(kwargs['name'])

    def _get_target_folder(self, *args, **kwargs):
        return self.drive_client.get_root_folder(kwargs['name'])

    def get_grids_rangs(self, *args, **kwargs):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        columnCount = kwargs['columnCount']
        rowCount = kwargs['rowCount']
        return 'A1:%(letter)s%(count)i' % {
            'letter': alphabet[columnCount - 1],
            'count': rowCount
        }

    def get_daily_data(self, *args, **kwargs):
        def is_daily_tab(item):
            return True if re.search(r'^Daily!(.+)$', item['range']).group(0) else False

        tab_data = list(filter(is_daily_tab, kwargs['data']['valueRanges']))[0]
        return tab_data['values'] if 'values' in tab_data else None

    def to_append_cell(self, row):
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
