#!/bin/bash

# Check if the correct number of arguments was provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <period>"
    exit 1
fi

# Check if the provided directory exists
if [ ! -d "$1" ]; then
    echo "Error: directory $1 does not exist"
    exit 1
fi

# Check if the provided period is a positive integer
if ! [[ "$2" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: period $2 is not a positive integer"
    exit 1
fi

directory=$1
period=$2

while true; do
    timestamp=$(date +%Y%m%d%H%M%S)
    touch "${directory}/file_${timestamp}"
    sleep $period
done
