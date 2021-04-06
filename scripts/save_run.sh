#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
RUN_DIR=$(pwd)/cache/run
RUN_ID=`cat ${RUN_DIR}/DATA_RUNID`
CURRENT_RUN_DIR=$(pwd)/cache/run-${RUN_ID}

CR=`tput setaf 1`
CG=`tput setaf 2`
CX=`tput sgr0`

echo Copying ${CG}${RUN_DIR}${CX} to ${CG}${CURRENT_RUN_DIR}${CX}
cp -r ${RUN_DIR} ${CURRENT_RUN_DIR}

UPLOAD_TARGET="sjtu-skyzh/[BUCKET NAME REDACTED]/run/${RUN_ID}"

echo Uploading to ${CG}${UPLOAD_TARGET}${CX}

MC_CLI=`$DIR/find_mc.sh`

if [ ! -z "$($MC_CLI ls $UPLOAD_TARGET)" ]; then
    echo ${CR}Run already exists on remote, please start a new run or change DATA_RUNID file.${CX}
    exit 1
fi

$MC_CLI mirror ${CURRENT_RUN_DIR}/ ${UPLOAD_TARGET}/

echo ${CG}Done.${CX}
