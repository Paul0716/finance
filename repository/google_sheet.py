from abstract.base import base
from adapter import google_sheet


class repository(base):

    def __init__(self, stock_number, *args, **kwargs):
        self.stock_number = stock_number
        self.adapter = google_sheet.adapter()
        super(base, self)

    def save(self, *args, **kwargs):
        self._batch_update_google_sheet(name=kwargs['name'], data=kwargs['data'])

    def get_date_list(self, *args, **kwargs):
        tab_title = 'Daily'
        stock_number = self.stock_number
        folder = self._get_target_folder(name=stock_number)
        sheet = self._get_target_sheet(name=stock_number)

        if sheet is None:
            sheet = self.drive_client.add_new_sheet(name=stock_number, parent=folder)

        # get target via google sheet API
        target = self.sheet_client.get(spreadsheetId=sheet['id'])
        sheet_prop = self.sheet_client.find_sheet_by_name(spreadsheet_properties=target, sheet_name=tab_title)

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
        return list(existing_data) if existing_data is not None else []

    def _batch_update_google_sheet(self, *args, **kwargs):
        tab_title = 'Daily'
        name = kwargs['name']
        folder = self._get_target_folder(name=name)
        sheet = self._get_target_sheet(name=name)
        if sheet is None:
            sheet = self.drive_client.add_new_sheet(name=name, parent=folder)

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
            sheet_prop = list(map(lambda response: response['addSheet'], response['replies']))

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
        append_data = list(map(self.adapter.to_append_cell, append_data))

        if len(append_data) > 0:
            self.sheet_client.appendCells(spreadsheetId=sheet['id'], body={
                'sheetId': sheet_prop[0]['properties']['sheetId'],
                'fields': '*',
                'rows': append_data
            })
