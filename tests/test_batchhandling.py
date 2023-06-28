import subprocess
import time
import pytest
import promptprocessing.batchhandling as bh

try:
    subprocess.check_output(['python', '../scripts/run_socket_batch.py', '-l', 'INFO'], stderr=subprocess.STDOUT)
    # subprocess.check_output(['python', '../scripts/run_socket_batch.py', '-l', 'INFO'])
    time.sleep(1)
except subprocess.CalledProcessError:
    print(f'Backend already running')

batch_handler = bh.SocketBatchHandler()


def test_submit_wo_id(my_task_1):
    with pytest.raises(RuntimeError):
        batch_handler.submit(my_task_1)


def test_submit(my_sleep_task):
    setattr(my_sleep_task, '_id', 42)  # to circumvent read-only id
    batch_handler.submit(my_sleep_task)
    assert 42 in batch_handler.get_running_ids()


# def test_increase_quota():
#     batch_handler.increase_quota()
