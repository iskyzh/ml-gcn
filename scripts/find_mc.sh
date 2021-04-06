#!/bin/bash

set -e

if command -v mc &> /dev/null
then
    echo mc
else
    if command -v mcli &> /dev/null
    then
        echo mcli
    else
        echo "Failed to find mc executable" >&2
        exit 1
    fi
fi
