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

### Usage
Prompt processing can be divided into three independent workflows: Registering new files,
managing the job queue, and adjusting the batch quota to regulate the backlog.
Each can be run as an independent cron job. An example cron config can be found
in `config/prompt-cron.txt`. Install it
like so
```shell
crontab scripts/scripts/prompt-cron.txt
```
Alternatively, 




```shell
source scripts/datagenerator/setup.sh
. scripts/datagenerator/venv/bin/activate
python scripts/datagenerator/generate_data.py
```

```shell
sh scripts/generate_files.sh <directory> <period[s]> <lifetime[m]>
```


```shell
sh scripts/generate_files.sh data/input/ 10 1
```
Would periodically create a new file in `data` and remove
every existing file that is older than 1 minute every 10 seconds.


```shell
python scripts/run_socket_batch.py
```

### Testing
```shell
cd tests/
pytest -s
```

