#!/bin/bash

DATE=$(date +"%Y%m%d_%H%M%S")
HOST=$(hostname | cut -c1-7)
GIT_HASH=$(git rev-parse --short HEAD)

if [[ $(git rev-parse --abbrev-ref HEAD) =~ ^train/(.*) ]]; then
    GIT_HASH="${BASH_REMATCH[1]}_${GIT_HASH}"
fi

if [[ $(git diff HEAD --stat) != '' ]]; then
    echo ${DATE}_${HOST}_${GIT_HASH}-dirty
else
    echo ${DATE}_${HOST}_${GIT_HASH}
fi
