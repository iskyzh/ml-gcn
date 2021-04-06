#/bin/bash

set -e

RUN_ID=$1

CR=`tput setaf 1`
CG=`tput setaf 2`
CX=`tput sgr0`

echo Peeking ${CG}$1${CX}

MCLI=`./scripts/find_mc.sh`

BASE="sjtu-skyzh/[BUCKET NAME REDACTED]/run"

$MCLI cat ${BASE}/${RUN_ID}/DATA_RUNID

echo ${CG}--- model ---${CX}

$MCLI cat ${BASE}/${RUN_ID}/DATA_MODEL_SUMMARY || true

echo

echo ${CG}--- train log ---${CX}

($MCLI cat ${BASE}/${RUN_ID}/train.log | column -t -s,) || true

echo ${CG}--- train weights ---${CX}

$MCLI ls ${BASE}/${RUN_ID}/checkpoints/ 

echo ${CG}--- other files ---${CX}

$MCLI ls ${BASE}/${RUN_ID}/
