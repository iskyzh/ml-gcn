#!/bin/bash

set -e 

RUN_DIR=$(pwd)/cache/run
RUN_ID=`cat ${RUN_DIR}/DATA_RUNID`

DIRTY=""
if [[ $(git diff HEAD --stat) != '' ]]; then
    DIRTY="-dirty"
fi

echo current git hash: `git rev-parse --short HEAD`$DIRTY, run_id: $RUN_ID
# read -p "Press [ENTER] "

rm cache/run/result-*.csv || true

python src/validate.py

for submission in $(ls cache/run/ | grep result-); do
    echo Submitting ${submission}
    kaggle competitions submit -f cache/run/${submission} cs410-2020-fall-ai-project-1 -m "$1"
    sleep 5    
done

kaggle competitions submissions cs410-2020-fall-ai-project-1 | head -n 20
