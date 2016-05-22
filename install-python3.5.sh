#!/bin/bash -e

EXPECTED_CHECKSUM=25094caf67eca28667c9122313b8f1b6ef935d35
FILENAME=python3.5_3.5.1~archiveteam20160521_i386.deb

if [ "`hostname`" != "warriorvm" ]; then
    echo "* Error: This does not appear to be a Warrior VM appliance. Exiting. *"
    exit 1
fi

if python3.5 --version; then
    echo "* The software is already installed. *"
    exit 0
fi

wget --directory-prefix /tmp/ --continue http://warriorhq.archiveteam.org/downloads/python/${FILENAME}

DOWNLOAD_CHECKSUM=`sha1sum /tmp/${FILENAME} | awk '{print $1}'`

echo "Checksum: ${EXPECTED_CHECKSUM} ${DOWNLOAD_CHECKSUM}"

if [ "${EXPECTED_CHECKSUM}" != "${DOWNLOAD_CHECKSUM}" ]; then
    echo "* Error: File checksum did not match. *"
    echo "Pausing for 60 seconds..."
    sleep 60
    exit 1
fi

sudo dpkg -i /tmp/${FILENAME}

echo "* Software installation finished. Please reboot for changes to take effect. *"
