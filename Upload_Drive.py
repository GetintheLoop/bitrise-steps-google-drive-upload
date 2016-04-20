from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload
import sys
import os
import urllib

BITRISEIO_DRIVE_SECRET_URL = os.environ.get('BITRISEIO_DRIVE_SECRET_URL')
BITRISE_IPA_PATH = os.environ.get('BITRISE_IPA_PATH')
GOOGLE_DRIVE_FOLDER_KEY = os.environ.get('GOOGLE_DRIVE_FOLDER_KEY')
BITRISE_DSYM_PATH = os.environ.get('BITRISE_DSYM_PATH')
APP_VERSION_NUMBER = os.environ.get('APP_VERSION_NUMBER') if os.environ.get('APP_VERSION_NUMBER') else '0'
APP_BUILD_NUMBER = os.environ.get('APP_BUILD_NUMBER') if os.environ.get('APP_BUILD_NUMBER') else '0'

secretFileName = "client_secret.json"
folder_id = GOOGLE_DRIVE_FOLDER_KEY

def downloadFileFromURL(url,fileName):
    downloadingFile = urllib.URLopener()
    downloadingFile.retrieve(url, fileName)

def getFileName(pathToIPA):
    if len(pathToIPA):
        list = pathToIPA.split('/')
        return list[-1]
    return ""

def upload(fileMetaDataList):
    scopes = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(secretFileName, scopes=scopes)
    http_auth = credentials.authorize(Http())
    service = discovery.build('drive', 'v3', http=http_auth)

    for fileMetaData in fileMetaDataList:
        fileMetaData['name']
        fileMetaData['path']
        fileMetaData['mimetype']

        file_metadata = {
          'name' : fileMetaData['name'],
          'parents': [ folder_id ]
        }

        media = MediaFileUpload(fileMetaData['path'],fileMetaData['mimetype'],resumable=True)

        print "Uploading {} to drive:".format(fileMetaData['name'])
        service.files().create(body=file_metadata,media_body=media,fields='id').execute()
        print 'Upload completed'

def getDefaultFileNameForiOSBuild(names):
    return "-".join(names)

IPAFileName = getFileName(BITRISE_IPA_PATH)
DSYMFileName = getFileName(BITRISE_DSYM_PATH)

if BITRISEIO_DRIVE_SECRET_URL:
    print "Downloading secret file"
    downloadFileFromURL(BITRISEIO_DRIVE_SECRET_URL,secretFileName)
    print "Download completed"

fileMetaDataList = []

IPAFileNameForUpload = getDefaultFileNameForiOSBuild([APP_VERSION_NUMBER,APP_BUILD_NUMBER,IPAFileName])
fileMetaData = {'name':IPAFileNameForUpload, 'path':BITRISE_IPA_PATH, 'mimetype':'application/zip'}
fileMetaDataList.append(fileMetaData)

DSYMFileNameForUpload = getDefaultFileNameForiOSBuild([APP_VERSION_NUMBER,APP_BUILD_NUMBER,DSYMFileName])
fileMetaData = {'name':DSYMFileNameForUpload, 'path':BITRISE_DSYM_PATH, 'mimetype':'application/zip'}
fileMetaDataList.append(fileMetaData)

for filePath in sys.argv[1:]:
    if filePath != "NOFILE":
        fileMetaData = {'name':getFileName(filePath), 'path':filePath, 'mimetype':'application/zip'}
        fileMetaDataList.append(fileMetaData)

upload(fileMetaDataList)
