import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

TARGET_FOLDER = 'Stock Report'

def authorization(scope, path='./client_secret.json'):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path, scope)
            creds = flow.run_local_server(port=0)
            print(creds)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def find_target_folder(items):
    def is_target_folder_exists(item):
        return item['mimeType'] == 'application/vnd.google-apps.folder' and item['name'] == TARGET_FOLDER
    files = list(filter(is_target_folder_exists, items))
    return files[0] if len(files) > 0 else None


def main():
    credentials = authorization(scope=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])

    # gspread client
    gc = build('sheets', 'v4', credentials=credentials)
    # google drive client
    gd = build('drive', 'v3', credentials=credentials)

    # drive list files
    results = gd.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])
    # check target folder
    folder = find_target_folder(items)

    if not folder:
        folder = gd.files().create(body={
            'name': TARGET_FOLDER,
            'mimeType': "application/vnd.google-apps.folder"
        }).execute()

    # Create new WorkSheet
    '''
    create by google drive
    '''
    # sheet = gd.files().create(body={
    #     'name': 'a new spreadsheet',
    #     'parents': [folder['id']],
    #     'description': 'a example worksheet',
    #     'mimeType': "application/vnd.google-apps.spreadsheet"
    # }).execute()
    # print(sheet)
    '''
    Or create by google sheet 
    '''
    sheet = gc.spreadsheets().create(body={
        'properties': {
            'title': 'a new spreadsheet',
        },
        'sheets':[
            {
                'properties': {
                    'title': '',
                    'index': 0,
                    'gridProperties': {
                        'rowCount': 4,
                        'columnCount': 4
                    }
                },
                "data": [
                    {
                        'startRow': 0,
                        'startColumn': 0,
                        'rowData': [
                            {
                                'values': [
                                    {
                                        'userEnteredValue': {
                                            'numberValue': 0
                                        }
                                    },
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
                        ]
                    }
                ],
            }
        ]
    }).execute()
    print(sheet)
    '''
    then move to parenet folder
    '''
    sh = gd.files().get(
        fileId=sheet['spreadsheetId']
    ).execute()
    sh['addParents'] = [folder['id']]
    print(sh,)
    request = gd.files().update(
        fileId=sheet['spreadsheetId'],
        body=sh
    )
    print(request)
    response = request.execute()
    print(response)


    # Update WorkSheet Data
    body = {
        'range': 'A1:D2',
        'majorDimension': 'ROWS',
        'values': [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
        ]
    }
    response = gc.spreadsheets().values().update(
        spreadsheetId=sheet['spreadsheetId'],
        valueInputOption='RAW',
        range='A1:D2',
        body=body
    ).execute()
    print(response)


    # Read Content of existing WorkSheet
    request = gc.spreadsheets().values().batchGet(
        spreadsheetId=response['spreadsheetId'],
        ranges='A1:D2',
        valueRenderOption='UNFORMATTED_VALUE',
        dateTimeRenderOption='FORMATTED_STRING')
    response = request.execute()
    print(response)

if __name__ == '__main__':
    main()