# Google Drive Upload Step #

This a step for Bitrise workflow, which allows upload a file to Google Drive

### Prerequisite ###

#### Go to Google Developers Console site do the following steps:
* Create a project
* Enable Drive API
* Create a service accounts in Permissions page, share the folder with this account
* And create a service account with key (For authentication)

#### Next:
* Upload your key to Bitrise Workflow Editor page under "Code signing & Files tab", and name it "BITRISEIO_DRIVE_SECRET_URL"
* Create GOOGLE_DRIVE_FOLDER_KEY under "App Env Vars", and set value as a folder key (Google Drive folder identifier)
