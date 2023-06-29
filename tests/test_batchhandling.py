import subprocess
import time
import pytest
from datetime import datetime
import promptprocessing.batchhandling as bh
from promptprocessing.task import Task


try:
    proc = subprocess.Popen(['python', '../scripts/run_socket_batch.py'],  # , '-l', 'INFO'])
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)
except Exception as e:
    print(f'Error occurred while starting backend: {e}')
    print(f'Backend probably already running...')


batch_handler = bh.SocketBatchHandler()
q_max = batch_handler.get_max_quota()
my_sleep_task = Task(input='_', output='_', command='sleep 0.1')
setattr(my_sleep_task, '_id', 42)  # to circumvent read-only id


def test_submit_wo_id(my_task_1):
    with pytest.raises(RuntimeError):
        batch_handler.submit(my_task_1)


def test_submit():
    batch_handler.submit(my_sleep_task)
    assert 42 in batch_handler.get_running_ids()
    while batch_handler.get_running_ids():  # make sure the job finishes
        time.sleep(0.01)


def test_set_quota():
    for q in range(1, q_max + 1):
        batch_handler.set_quota(q)
        assert batch_handler.get_quota() == q
    batch_handler.set_quota(q_max + 1)
    assert batch_handler.get_quota() == q_max


def test_increase_quota():
    batch_handler.set_quota(0)
    for i in range(q_max):
        batch_handler.increase_quota()
        assert batch_handler.get_quota() == i + 1
    batch_handler.increase_quota()
    assert batch_handler.get_quota() == q_max


def test_decrease_quota():
    batch_handler.set_quota(q_max)
    for i in range(q_max):
        batch_handler.decrease_quota()
        assert batch_handler.get_quota() == q_max - i - 1
    batch_handler.decrease_quota()
    assert batch_handler.get_quota() == 0


@pytest.mark.parametrize(
    "quota,number_of_tasks,expected_duration",
    [
        (1, 1, 0.1),
        (1, 5, 0.5),
        (5, 1, 0.1),
        (5, 5, 0.1),
    ],
)
def test_duration(quota, number_of_tasks, expected_duration):
    batch_handler.set_quota(quota)
    [batch_handler.submit(my_sleep_task) for _ in range(number_of_tasks)]
    t_0 = datetime.now()
    while batch_handler.get_running_ids():
        time.sleep(0.01)
    duration = (datetime.now() - t_0).microseconds / 1000000
    assert duration == pytest.approx(expected_duration, 0.5)
