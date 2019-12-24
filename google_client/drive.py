from googleapiclient.discovery import build

from .utils import authorization


class google_drive:
    _root_files = []

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

    def _find_target(self, type, name):
        def is_target_exists(item):
            return item['mimeType'] == type and item['name'] == name

        files = list(filter(is_target_exists, self._root_files))
        return files[0] if len(files) > 0 else None

    def find_target_sheet(self, sheet_name):
        return self._find_target('application/vnd.google-apps.spreadsheet', sheet_name)

    def find_target_folder(self, folder_name):
        return self._find_target('application/vnd.google-apps.folder', folder_name)

    def get_root_folder(self, folder_name):
        # drive list files
        results = self.client.files().list(fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])
        self._root_files = items

        # check target folder
        folder = self.find_target_folder(folder_name)
        if not folder:
            folder = self.client.files().create(body={
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }).execute()
        return folder

    def add_new_sheet(self, *args, **kwargs):
        name = kwargs['name']
        parent = kwargs['parent'] if 'parent' in kwargs else None

        return self.client.files().create(body={
            'name': name,
            'parents': [parent['id']],
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }).execute()

    def create(self, body):
        return self.client.files().create(body=body).execute()
