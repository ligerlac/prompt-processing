from datetime import datetime
from dataclasses import dataclass, field, fields
from typing import List, Optional

valid_statuses = ['unfinished', 'fail', 'success']


@dataclass
class Task:
    """
    e.g. <python analyze.py data/input/file_203.root --output data/output/file_203_processed.root
    """
    input: str
    output: str
    command: str
    n_tries: int = 0
    max_tries: int = 3
    created: datetime = field(default_factory=datetime.now)
    status: str = 'unfinished'
    _id: int | None = None
    # _status: str = 'waiting'
    # _id: int | None = None
    #
    # def __post_init__(self):
    #     if self._status not in valid_statuses:
    #         raise ValueError(f'not a valid status: {self._status}. must be one of {valid_statuses}')

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value):
        raise RuntimeError('<Task.id> is a read-only attribute')

    # @property
    # def status(self) -> str:
    #     return self._status
    #
    # @status.setter
    # def status(self, value):
    #     if value not in valid_statuses:
    #         raise ValueError(f'not a valid status: {value}. must be one of {valid_statuses}')
    #     self._status = value

    @classmethod
    def get_field_names(cls):
        # return [fld.name for fld in fields(cls)]
        d = [fld.name for fld in fields(cls)]
        d.remove('_id')
        return d

    def get_dict_wo_id(self):
        d = self.__dict__.copy()
        del d['_id']
        return d


# class TaskCreator:
#     def __init__(self):
#         pass