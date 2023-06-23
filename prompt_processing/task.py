from datetime import datetime
from dataclasses import dataclass, field, fields
from typing import List, Optional

valid_statuses = ['waiting', 'running', 'fail', 'success']


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
    created: datetime = field(default_factory=lambda: datetime.now())
    _status: str = 'waiting'

    def __post_init__(self):
        if self._status not in valid_statuses:
            raise ValueError(f'not a valid status: {self._status}. must be one of {valid_statuses}')

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value):
        if value not in valid_statuses:
            raise ValueError(f'not a valid status: {value}. must be one of {valid_statuses}')
        self._status = value

    @classmethod
    def get_field_names(cls):
        return [fld.name for fld in fields(cls)]
