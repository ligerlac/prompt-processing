import subprocess
import time
import pytest
import prompt_processing.batchhandling as bh


subprocess.Popen(['python', '../scripts/run_socket_batch.py'])
time.sleep(1)

batch_handler = bh.SocketBatchHandler()


def test_submit_wo_id(my_task_1):
    with pytest.raises(RuntimeError):
        batch_handler.submit(my_task_1)


def test_submit(my_sleep_task):
    setattr(my_sleep_task, '_id', 42)  # to circumvent read-only id
    batch_handler.submit(my_sleep_task)
    print(f'batch_handler.get_running() = {batch_handler.get_running()}')
