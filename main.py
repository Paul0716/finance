from pprint import pprint
from google_client.sheets import google_sheets
from google_client.drive import google_drive

TARGET_FOLDER = 'Stock Report'


def main():
    scope=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    sheets_client = google_sheets(scope, path='./client_secret.json')

    # google drive client
    drive_client = google_drive(scope, path='./client_secret.json')

    folder = drive_client.get_root_folder(TARGET_FOLDER)

    # Create new WorkSheet
    '''
    create by google drive
    '''
    sheet = drive_client.create(body={
        'name': 'a new spreadsheet',
        'parents': [folder['id']],
        'description': 'a example worksheet',
        'mimeType': "application/vnd.google-apps.spreadsheet"
    })

    # add a target worksheet
    response = sheets_client.addSheet(spreadsheetId=sheet['id'], body={
        'properties': {
            'index': 0,
            'title': 'Deposits',
            'gridProperties': {
                'rowCount': 20,
                'columnCount': 12
            },
            'tabColor': {
                'red': 1.0,
                'green': 0.3,
                'blue': 0.4
            }
        },
    })
    pprint(response)

    target = sheets_client.get(spreadsheetId=sheet['id'])

    sheet_prop = sheets_client.find_sheet_by_name(spreadsheet_properties=target, sheet_name ='Deposits')
    pprint(sheet_prop)

    # Update WorkSheet Data
    response = sheets_client.values_update(spreadsheetId=sheet['id'], valueInputOption='RAW', range='A1:D2', body={
        'range': 'A1:D2',
        'majorDimension': 'ROWS',
        'values': [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
        ]
    });
    pprint(response)

    # Apeend WorkSheetData
    sheets_client.appendCells(spreadsheetId=sheet['id'], body={
        'sheetId': sheet_prop['properties']['sheetId'],
        'rows': [
            {
                'values': [
                    {
                        'userEnteredValue': {
                            'numberValue': 1
                        }
                    },
                    {
                        'userEnteredValue': {
                            'numberValue': 2
                        }
                    },
                    {
                        'userEnteredValue': {
                            'numberValue': 3
                        }
                    }
                ]
            }
        ],
        'fields': '*'
    })
    pprint(response)

    # Read Content of existing WorkSheet
    # request = gc.spreadsheets().values().batchGet(
    #     spreadsheetId=response['spreadsheetId'],
    #     ranges='A1:D2',
    #     valueRenderOption='UNFORMATTED_VALUE',
    #     dateTimeRenderOption='FORMATTED_STRING')
    # response = request.execute()
    response = sheets_client.read(spreadsheetId=response['spreadsheetId'],
        ranges='A1:D2',
        valueRenderOption='UNFORMATTED_VALUE',
        dateTimeRenderOption='FORMATTED_STRING')

    pprint(response)

if __name__ == '__main__':
    main()