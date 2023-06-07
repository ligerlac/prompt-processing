#!/bin/bash

# Check if the correct number of arguments was provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <directory> <period> <lifetime>"
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

# Check if the provided lifetime is a positive integer
if ! [[ "$3" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: lifetime $3 is not a positive integer"
    exit 1
fi

directory=$1
period=$2
lifetime=$3

while true; do
    timestamp=$(date +%Y%m%d%H%M%S)
    touch "${directory}/file_${timestamp}"

    # Convert lifetime in seconds to minutes as that's what find -mmin expects
    lifetime_in_minutes=$((lifetime / 60))

    # Find and remove files in the directory that are older than the specified lifetime
    find "$directory" -type f -mmin +$lifetime_in_minutes -exec rm -f {} \;

    sleep $period
done
