import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

def main():
    print('main function')

    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('./service.json', scope)
    # gspread client
    # gc = gspread.authorize(credentials)
    # google drive client
    gd = build('drive', 'v3', credentials=credentials)



    '''
    google drive
    '''
    # print(gd)
    # body = {
    #     'name': 'test-folder',
    #     'mimeType': "application/vnd.google-apps.folder"
    # }
    # folder = gd.files().create(body=body).execute()
    results = gd.files().list(pageSize=20, fields="nextPageToken, files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1}) mimeType:{2}'.format(item['name'], item['id'], item['mimeType']))
            if not item['mimeType'] is 'application/vnd.google-apps.folder':
                file = gd.files().update(fileId=item['id'], addParents='1yxXav3_OeHickPbgNgfRiv01gdZGgNRZ', fields='id').execute()



    # Create new WorkSheet
    # sh = gc.create('A new spreadsheet')
    # sh.share('justlove0714@gmail.com', perm_type='user', role='writer')
    # worksheet = sh.add_worksheet(title="A worksheet", rows="100", cols="20")
    # cell_list = worksheet.range('A1:C7')
    #
    # for cell in cell_list:
    #     cell.value = 'O_o'

    # Update in batch
    # worksheet.update_cells(cell_list)

if __name__ == '__main__':
    main()