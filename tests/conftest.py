import pytest
import datetime
from prompt_processing.task import Task


@pytest.fixture(scope='module')
def my_task_1():
    return Task(input='data/input/test_file_1.root',
                output='data/output/test_file_1_processed.root',
                command='python scripts/analyze.py data/input/test_file_1.root')


@pytest.fixture(scope='module')
def my_task_2():
    return Task(input='data/input/test_file_2.root',
                output='data/output/test_file_2_processed.root',
                command='python scripts/analyze.py data/input/test_file_2.root',
                created=datetime.datetime.now() - datetime.timedelta(days=2))
