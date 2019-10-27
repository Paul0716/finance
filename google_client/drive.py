from googleapiclient.discovery import build
from .utils import authorization

class google_drive:
    def __init__(self, scope, path):
        '''
        constructor
        :param scope: google api authorization scope
        :param path: credentials.json file path
        '''
        self.authorization(scope, path)
        self.client = self.build()

    def authorization(self, scope, path):
        self.credentials = authorization(scope, path)


    def build(self):
        return build('drive', 'v3', credentials=self.credentials)

    def find_target_folder(self, items, folder_name):
        def is_target_folder_exists(item):
            return item['mimeType'] == 'application/vnd.google-apps.folder' and item['name'] == folder_name

        files = list(filter(is_target_folder_exists, items))
        return files[0] if len(files) > 0 else None

    def get_root_folder(self, folder_name):
        # drive list files
        results = self.client.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        # check target folder
        folder = self.find_target_folder(items, folder_name)

        if not folder:
            folder = self.client.files().create(body={
                'name': folder_name,
                'mimeType': "application/vnd.google-apps.folder"
            }).execute()
        return folder

    def create(self, body):
        return self.client.files().create(body=body).execute()