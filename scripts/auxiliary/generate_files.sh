#!/bin/bash

# Check if the correct number of arguments was provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <directory> <period>[s] <lifetime>[m]"
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

# Check if the provided lifetime is larger than the period
if ! ((60*$3 > $2)); then
    echo "Error: lifetime ($3)m must be larger than creation period ($2)s"
    exit 1
fi

directory=$1
period=$2
lifetime=$3

while true; do
    timestamp=$(date +%Y%m%d%H%M%S)
    touch "${directory}/file_${timestamp}.root"

    find "$directory" -type f -mmin +$lifetime -exec rm -f {} \;

    sleep $period
done
