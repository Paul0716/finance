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
    sheet = gd.files().create(body={
        'name': 'a new spreadsheet',
        'parents': [folder['id']],
        'description': 'a example worksheet',
        'mimeType': "application/vnd.google-apps.spreadsheet"
    }).execute()
    print(sheet)

    body = {
        'range': 'A1:D2',
        'majorDimension': 'ROWS',
        'values': [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
        ]
    }
    # Update WorkSheet Data
    result = gc.spreadsheets().values().update(
        spreadsheetId=sheet['id'],
        valueInputOption='RAW',
        range='A1:D2',
        body=body
    ).execute()
    print(result)

    # Read Content of existing WorkSheet

if __name__ == '__main__':
    main()