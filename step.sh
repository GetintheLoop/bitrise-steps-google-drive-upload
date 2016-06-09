#!/bin/bash
THIS_SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRIVE_API_LIB_PATH="${THIS_SCRIPTDIR}/libs/drive_api"

if $BITRISE_CLI = 'true'; then
  DRIVE_API_LIB_PATH=$PATH_TO_GOOGLE_API_INSTALLER
fi

echo "Installing Google Drive python Library..."
(cd "${DRIVE_API_LIB_PATH}" && python setup.py install --user)

echo "Drive Library installed"

echo "Running script..."

FILES=(${file1} ${file2} ${file3})

python "${THIS_SCRIPTDIR}/Upload_Drive.py" ${FILES[*]}
