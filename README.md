Prompt processing of protoDUNE data

```shell
source scripts/datagenerator/setup.sh
. scripts/datagenerator/venv/bin/activate
python scripts/datagenerator/generate_data.py
```

```shell
sh scripts/generate_files.sh <directory> <period[s]> <lifetime[m]>
```


```shell
sh scripts/generate_files.sh data/ 10 1
```
Would periodically create a new file in `data` and remove
every existing file that is older than 1 minute every 10 seconds.


```shell
python scripts/run_socket_batch.py
```