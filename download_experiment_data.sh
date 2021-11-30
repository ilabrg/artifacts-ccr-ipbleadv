#!/bin/sh

BASEDIR=$(dirname "${0}")
URL=https://box.fu-berlin.de/s/2JJNWz5fDZ5jpyc/download/ccr_ipbleadv_logs.zip
LOGDIR="./results/logs"
TMPFILE="logs.zip"

if [ ! -e ${LOGDIR} ]; then
    echo "Please execute this script from the root of the repository"
    exit 1
fi

wget -O ${LOGDIR}/${TMPFILE} ${URL}
unzip ${LOGDIR}/${TMPFILE} -d ${LOGDIR}
rm ${LOGDIR}/${TMPFILE}
