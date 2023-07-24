## Welcome to promptprocessing!
### Table of contents
* [Introduction](#intro)
* [Setup](#setup)
* [Usage](#usage)
* [Testing](#testing)

### Introduction
This is a prototype of a production system for prompt processing of ProtoDUNE data.

[//]: # (The functionality is implemented in three distinct modules: `bookkeeping`,)

[//]: # (`batchhandling`, and `filehandling`. )

### Setup
```shell
python -m venv venv/
. venv/bin/activate
pip install -r requirements.txt
```

### Configuration
Configuration happens via `.yaml` files. An example can be found in
`config/local.yaml`.

### Usage
Prompt processing can be divided into three independent workflows: Registering new files,
managing the job queue, and adjusting the batch quota to regulate the backlog.
Each can be run as an independent cron job. An example cron config can be found
in `config/prompt-cron.txt`. Install it like so
```shell
crontab scripts/scripts/prompt-cron.txt
```
Alternatively, the python script can be called directly
```shell
python run.py --workflow loop-all
```

### Run in local dummy mode
Prompt-processing can be run locally in a dummy-mode with the help
of a couple auxiliary scripts. Firstly, activate a data generator
that spawns in deletes file in a specified directory, simulating the
flow of raw data in and out of the disk buffer:
```shell
source scripts/datagenerator/setup.sh <spawnrate[s]> <lifetime[m]>
```
Next, start the backend of the batch simulator, SocketBatch:
```shell
python scripts/run_socket_batch.py
```
The last component is a dummy script that sleeps for a user-specified
period of time and randomly succeeds with a user-specified probability.
It can be found in `scripts/auxiliary/analyze.py`.

### Testing
Unit tests can be run via
```shell
cd tests/
pytest -s
```
