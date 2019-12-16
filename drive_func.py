from __future__ import print_function
import httplib2
from apiclient import discovery
from oauth2client import client,tools
from oauth2client.file import Storage
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
import io,os
#Done with all the required import................


class gdrive:


    def __init__(self):

    # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('drive', 'v3', credentials=self.creds)



    def uploadconverted(self,filepath):

        file_metadata = {
        'name': 'thebegginging',
        'mimeType': 'application/vnd.google-apps.document'
        }
        media = MediaFileUpload(filepath,                                        #############################################################
                                mimetype='application/pdf',                        # CONVERTING AN IMAGE INTO GOOGLE DOCS FORMAT THEN UPLOADING#
                                resumable=True)                                    #############################################################
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        # print ('File ID: %s' % file.get('id'))
        print("Upload 100%")
        return (file.get('id'))





    def download(self,file_id,filepath):
        request = self.service.files().export_media(fileId=file_id,mimeType='text/plain')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False                                                            ##################################################
        while done is False:                                                    # FINALLY DOWNLOADING ONLY THE OC RECOGNISED FILE#
            status, done = downloader.next_chunk()                              ##################################################
            print ("Download %d%%." % int(status.progress() * 100))

        with io.open(filepath,'wb') as f:
            fh.seek(0)
            f.write(fh.read())


