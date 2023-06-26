import prompt_processing.bookkeeping as bk
from prompt_processing.task import Task
import tempfile
import datetime


temp_file = tempfile.NamedTemporaryFile()
book_keeper = bk.LocalBookKeeper(temp_file.name)

print(f'book_kepper.df =\n{book_keeper.df}')

t1 = Task(input='data/input/test_file.root',
          output='data/output/test_file_processed.root',
          command='python scripts/analyze.py data/input/test_file.root')
t2 = Task(input='data/input/test_file.root',
          output='data/output/test_file_processed.root',
          command='python scripts/analyze.py data/input/test_file.root',
          created=datetime.datetime.now() - datetime.timedelta(days=2))


def test_add_task():
    book_keeper.add([t2, t1])
    read_back = book_keeper.get()
    assert len(read_back) == 1
    t1_re = read_back[0]
    assert t1_re.id
    assert t1_re.get_dict_wo_id() == t1.get_dict_wo_id()
#
#
# def test_update():
#     t2.command = 'updated command'
#     book_keeper.update([t2])
