# import pytest
# from prompt_processing.task import Task
#
#
# def test_assign_id(my_task_1):
#     with pytest.raises(RuntimeError):
#         my_task_1.id = 42
#
#
# def test_get_field_names():
#     assert 'id' not in Task.get_field_names()
#
#
# def test_get_dict(my_task_1):
#     d = my_task_1.get_dict_wo_id()
#     for key, value in d.items():
#         assert my_task_1.__dict__[key] == d[key]
#     assert 'id' not in my_task_1.get_dict_wo_id()
