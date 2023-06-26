from prompt_processing.task import Task

# t1 = Task(input='data/input/test_file.root',
#           output='data/output/test_file_processed.root',
#           command='python scripts/analyze.py data/input/test_file.root')
#
#
# # def test_get_field_names():
# #     assert 'id' not in Task.get_field_names()
#
#
# def test_get_dict():
#     d = t1.get_dict_wo_id()
#     for key, value in d.items():
#         assert t1.__dict__[key] == d[key]
#     assert 'id' not in t1.get_dict_wo_id()
