import prompt_processing.bookkeeping as bk
from prompt_processing.task import Task
import tempfile
import datetime
from dataclasses import fields


temp_file = tempfile.NamedTemporaryFile()
book_keeper = bk.LocalBookKeeper(temp_file.name)


def test_add_task():
    t = Task(input='data/input/test_file.root',
             output='data/output/test_file_processed.root',
             command='python scripts/analyze.py data/input/test_file.root')
    book_keeper.add([t])
    t2 = Task(input='data/input/test_file.root',
              output='data/output/test_file_processed.root',
              command='python scripts/analyze.py data/input/test_file.root',
              created=datetime.datetime.now() - datetime.timedelta(days=2))
    book_keeper.add([t2])
    # print(f'book_keeper.get() = {book_keeper.get(dt=datetime.timedelta(days=3))}')
    print(f'book_keeper.get() = {book_keeper.get()}')
    # assert book_keeper.get()
    # book_keeper.add([t])
    # print(' ')
    # print(book_keeper.df)
