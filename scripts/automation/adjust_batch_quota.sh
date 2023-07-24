#!/bin/bash

# Determine the absolute path of the code base
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." >/dev/null 2>&1 && pwd )"

# Execute your command
#$DIR/your-command
$DIR/venv/bin/python $DIR/run.py --workflow adjust-batch-quota --config $DIR/config/local.yaml
