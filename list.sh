#!/bin/bash

set -e

MCLI=`./scripts/find_mc.sh`

$MCLI ls sjtu-skyzh/[BUCKET NAME REDACTED]/run/ | awk '{print $NF}' | sed 's/\/$//'
