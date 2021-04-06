#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

RUN_ID=`$DIR/generate_run_id.sh`

CR=`tput setaf 1`
CG=`tput setaf 2`
CX=`tput sgr0`

echo Run ID: ${CG}${RUN_ID}${CX}

RUN_DIR=$(pwd)/cache/run
CURRENT_RUN_DIR=$(pwd)/cache/run-${RUN_ID}

if [ ! -d $RUN_DIR ]; then
    echo $RUN_DIR not exist, will create one.
else
    if [ -f ${RUN_DIR}/DATA_RUNID ]; then
        PREV_RUN_ID=`cat ${RUN_DIR}/DATA_RUNID`
        echo $RUN_DIR already exists with ${CR}${PREV_RUN_ID}${CX}, all data will be purged. Press enter to continue, or Ctrl+C to cancel.
    else
        echo $RUN_DIR already exists with no run information, all data will be purged. Press enter to continue, or Ctrl+C to cancel
    fi
    read -p "Press [ENTER] "
    rm -rf $RUN_DIR
fi

mkdir $RUN_DIR

echo $RUN_ID > $RUN_DIR/DATA_RUNID
