#!/bin/bash

THIS_SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DRIVE_API_LIB_PATH="${THIS_SCRIPTDIR}/libs/drive_api"
cd "${DRIVE_API_LIB_PATH}"

echo "Installing Google Drive python Library..."
python setup.py install --user
echo "Drive Library installed"

cd "${THIS_SCRIPTDIR}"
echo "Running script..."

# export variables for python script
export BITRISEIO_DRIVE_SECRET_URL
export GOOGLE_DRIVE_FOLDER_KEY
export BITRISE_IPA_PATH
export BITRISE_DSYM_PATH
export APP_VERSION_NUMBER
export APP_BUILD_NUMBER
export uploadBuildFiles

FILES=(${file1} ${file2} ${file3})

python Upload_Drive.py ${FILES[*]}
