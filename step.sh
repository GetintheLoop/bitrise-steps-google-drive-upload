#!/bin/bash
THIS_SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRIVE_API_LIB_PATH="${THIS_SCRIPTDIR}/drive_api"
cd "${DRIVE_API_LIB_PATH}"

echo "Installing Google Drive python Library..."
python setup.py install --user
echo "Drive Library installed"
cd "${THIS_SCRIPTDIR}"
echo "Running script..."
python Upload_Drive.py "${BITRISEIO_DRIVE_SECRET_URL}" "${BITRISE_IPA_PATH}" "${GOOGLE_DRIVE_FOLDER_KEY}" "${BITRISE_BUILD_NUMBER}" "${GIT_CLONE_COMMIT_HASH}" "${BITRISE_DSYM_PATH}" "${APP_VERSION_NUMBER}" "${APP_BUILD_NUMBER}"
