from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient import discovery
from apiclient import errors
from apiclient.http import MediaFileUpload
import sys
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

BITRISEIO_DRIVE_SECRET_URL = sys.argv[1]
BITRISE_IPA_PATH = sys.argv[2]
GOOGLE_DRIVE_FOLDER_KEY = sys.argv[3]
BITRISE_BUILD_NUMBER = sys.argv[4]
BITRISE_GIT_COMMIT = sys.argv[5]
BITRISE_DSYM_PATH = sys.argv[6]
APP_VERSION_NUMBER = sys.argv[7]
APP_BUILD_NUMBER = sys.argv[8]

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
