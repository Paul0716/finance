from google_client.sheets import google_sheets
from google_client.drive import google_drive
from pprint import pprint

class abstract_report:
    target_folder = 'Taiwan Index Stock'
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    sheet_client = google_sheets(scope, path='./client_secret.json')
    drive_client = google_drive(scope, path='./client_secret.json'

    def _get_target_sheet(self):
        return self.drive_client.find_target_sheet(self.stock_number)

    def _get_target_folder(self):
        return self.drive_client.get_root_folder(self.target_folder)

    def get_grids_rangs(self, *args, **kwargs):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        columnCount = kwargs['columnCount']
        rowCount = kwargs['rowCount']
        return 'A1:%(letter)s%(count)i' % {
            'letter': alphabet[columnCount - 1],
            'count': rowCount
        }