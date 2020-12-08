# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import mimetypes
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def pathToDirs(path):
    # remove preceeding /
    if path[0] == "/":
        path = path[1:]

    return path.split('/')

class Drive:
    def __init__(self):
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
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def _listFoldersInFolder(self, folder_id):
        """
        Returns a list of sub-folders, where each folder is represented by a
        dictionary with keys 'id' and 'name'.
        """

        query = "mimeType='application/vnd.google-apps.folder' and parents in '"+folder_id+"' and trashed = false"
        results = self.service.files().list(
            q=query,
            fields="nextPageToken, files(id, name)",
            pageSize=400
        ).execute()

        return results.get('files', [])

    def _getFolderID(self, path):
        dirs = pathToDirs(path)
        return self._getFolderIDHelper(dirs)

    def _getFolderIDHelper(self, dirs, folder_id='root', path=''):
        """
        Returns the id of the folder that is located at the bottom of the
        list of directories.
        """

        # base case
        if len(dirs) == 0:
            return folder_id

        # the path that we are about to try to find
        new_path = path + "/" + dirs[0]

        # get all of the folders in path
        folders = self._listFoldersInFolder(folder_id)

        for folder in folders:
            if folder['name'] == dirs[0]:
                return self._getFolderIDHelper(
                    dirs[1:],
                    folder_id=folder['id'],
                    path=new_path,
                )

        raise Exception(f'No such folder: {new_path}')


    def _makePictureName(self):
        """
        Makes a picture name using the current timestamp:
            YYYY-MM-DD HH:MM:SS:MMM
        """
        now = datetime.now() # current date and time

        return now.strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]


    def uploadPicture(self, source_file):
        picture_name = self._makePictureName()
        self.uploadFile(source_file, '/Personal/webcam-pictures', picture_name)
        return picture_name

    def uploadFile(self, source_filepath, destination_directory, destintion_filename):
        mimetype, _ = mimetypes.guess_type(source_filepath)

        folder_id = self._getFolderID(destination_directory)
        file_metadata = {
            'name': destintion_filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(source_filepath,
                                mimetype=mimetype,
                                resumable=True)

        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()


def main():
    d = Drive()
    d.uploadPicture('test_img.jpg')


if __name__ == '__main__':
    main()
