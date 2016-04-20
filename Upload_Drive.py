from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload
import sys
import os
import urllib

def downloadFileFromURL(url,fileName):
    downloadingFile = urllib.URLopener()
    downloadingFile.retrieve(url, fileName)

def getIPAFileName(pathToIPA):
    if len(pathToIPA):
        list = pathToIPA.split('/')
        return list[-1]
    return ""

def upload(service, fileNameForUpload, localPath, folderId, mimetype):
    file_metadata = {
      'name' : fileNameForUpload,
      'parents': [ folderId ]
    }
    media = MediaFileUpload(localPath,mimetype,resumable=True)

    print "Uploading {} to drive:".format(fileNameForUpload)
    service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    print 'Upload completed'

BITRISEIO_DRIVE_SECRET_URL = os.environ.get('BITRISEIO_DRIVE_SECRET_URL')
BITRISE_IPA_PATH = os.environ.get('BITRISE_IPA_PATH')
GOOGLE_DRIVE_FOLDER_KEY = os.environ.get('GOOGLE_DRIVE_FOLDER_KEY')
BITRISE_DSYM_PATH = os.environ.get('BITRISE_DSYM_PATH')
APP_VERSION_NUMBER = os.environ.get('APP_VERSION_NUMBER')
APP_BUILD_NUMBER = os.environ.get('APP_BUILD_NUMBER')

IPAFileName = getIPAFileName(BITRISE_IPA_PATH)
DSYMFileName = getIPAFileName(BITRISE_DSYM_PATH)

print "Downloading secret file"
secretFileName = "client_secret.json"
downloadFileFromURL(BITRISEIO_DRIVE_SECRET_URL,secretFileName)
print "Download completed"

scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(secretFileName, scopes=scopes)
http_auth = credentials.authorize(Http())
service = discovery.build('drive', 'v3', http=http_auth)
folder_id = GOOGLE_DRIVE_FOLDER_KEY

IPAFileNameForUpload = "{}-{}-{}".format(APP_VERSION_NUMBER,APP_BUILD_NUMBER,IPAFileName)
upload(service, IPAFileNameForUpload, BITRISE_IPA_PATH, folder_id, 'application/zip')

DSYMFileNameForUpload = "{}-{}-{}".format(APP_VERSION_NUMBER,APP_BUILD_NUMBER,DSYMFileName)
upload(service, DSYMFileNameForUpload, BITRISE_IPA_PATH, folder_id, 'application/zip')
