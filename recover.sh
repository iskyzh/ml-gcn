#/bin/bash

RUN_ID=$1

CR=`tput setaf 1`
CG=`tput setaf 2`
CX=`tput sgr0`

echo Recovering ${CG}$1${CX}

RUN_DIR=$(pwd)/cache/run

if [ -d $RUN_DIR ]; then
    if [ -f ${RUN_DIR}/DATA_RUNID ]; then
        PREV_RUN_ID=`cat ${RUN_DIR}/DATA_RUNID`
        echo $RUN_DIR already exists with ${CR}${PREV_RUN_ID}${CX}, all data will be purged. Press enter to continue, or Ctrl+C to cancel.
    else
        echo $RUN_DIR already exists with no run information, all data will be purged. Press enter to continue, or Ctrl+C to cancel
    fi
    read -p "Press [ENTER] "
    rm -rf $RUN_DIR
fi

MCLI=`./scripts/find_mc.sh`

$MCLI mirror --overwrite sjtu-skyzh/[BUCKET NAME REDACTED]/run/${RUN_ID} $(pwd)/cache/run-${RUN_ID}
rsync -r $(pwd)/cache/run-${RUN_ID}/ ${RUN_DIR}
