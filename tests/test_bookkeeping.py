import promptprocessing.bookkeeping as bk
import datetime
import tempfile


temp_file = tempfile.NamedTemporaryFile()
book_keeper = bk.LocalBookKeeper(temp_file.name)


def test_add_task(my_task_1):
    book_keeper.add([my_task_1])
    read_back = book_keeper.get()
    assert len(read_back) == 1
    t1_re = read_back[0]
    assert t1_re.id is not None
    assert t1_re.get_dict_wo_id() == my_task_1.get_dict_wo_id()


def test_read_back_date(my_task_1, my_task_2):
    book_keeper.add([my_task_2])
    read_back = book_keeper.get()
    assert len(read_back) == 1
    read_back = book_keeper.get(dt=datetime.timedelta(days=5))
    assert len(read_back) == 2


def test_update():
    task = book_keeper.get()[0]
    task.command = 'updated command'
    book_keeper.update([task])
    task_re = book_keeper.get()[0]
    assert task_re.command == 'updated command'


def test_read_back_status(my_successful_task):
    book_keeper.add([my_successful_task])
    read_back = book_keeper.get(status='success')
    for t in read_back:
        assert t.status == 'success'
    assert read_back[0].get_dict_wo_id() == my_successful_task.get_dict_wo_id()
