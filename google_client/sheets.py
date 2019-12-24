from googleapiclient.discovery import build

from .utils import authorization, find_sheet_by_name


class google_sheets:
    def __init__(self, scope, path):
        '''
        constructor
        :param scope: google api authorization scope
        :param path: credentials.json file path
        '''
        self.authorization(scope, path)
        self.client = self.build().spreadsheets()

    def authorization(self, scope, path):
        self.credentials = authorization(scope, path)

    def build(self):
        return build('sheets', 'v4', credentials=self.credentials)

    def _batchUpdate(self, spreadsheetId, body):
        return self.client \
            .batchUpdate(spreadsheetId=spreadsheetId, body=body) \
            .execute()

    def _values_batch_get(self, spreadsheetId, ranges, valueRenderOption, dateTimeRenderOption):
        return self.client \
            .values() \
            .batchGet(spreadsheetId=spreadsheetId,
                      ranges=ranges,
                      valueRenderOption=valueRenderOption,
                      dateTimeRenderOption=dateTimeRenderOption) \
            .execute()

    def get(self, spreadsheetId):
        return self.client \
            .get(spreadsheetId=spreadsheetId).execute()

    def find_sheet_by_name(self, spreadsheet_properties, sheet_name):
        return find_sheet_by_name(spreadsheet_properties, sheet_name)

    def values_update(self, spreadsheetId, valueInputOption, range, body):
        return self.client \
            .values() \
            .update(spreadsheetId=spreadsheetId,
                    valueInputOption=valueInputOption,
                    range=range,
                    body=body) \
            .execute()

    def addSheet(self, spreadsheetId, body):
        return self._batchUpdate(spreadsheetId=spreadsheetId, body={
            'requests': [
                {
                    'addSheet': body
                }
            ]
        })

    def appendCells(self, spreadsheetId, body):
        return self._batchUpdate(spreadsheetId=spreadsheetId, body={
            'requests': [
                {
                    'appendCells': body
                }
            ]
        })

    def read(self, spreadsheetId, ranges, valueRenderOption, dateTimeRenderOption):
        return self._values_batch_get(spreadsheetId=spreadsheetId,
                                      ranges=ranges,
                                      valueRenderOption=valueRenderOption,
                                      dateTimeRenderOption=dateTimeRenderOption)
