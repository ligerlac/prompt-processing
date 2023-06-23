import abc
import datetime
from prompt_processing.task import Task
import pandas as pd


class BookKeeper(abc.ABC):
    """
    keeps a collection of tasks
    """
    def update(self, task_list: list[Task]) -> None:
        self._update([t.__dict__ for t in task_list])

    def add(self, task_list: list[Task]) -> None:
        self._add([t.__dict__ for t in task_list])

    def get(self, dt=datetime.timedelta(days=1)) -> list[Task]:
        raise NotImplementedError

    def _update(self, dict_list: list[dict]) -> list[dict]:
        raise NotImplementedError

    def _add(self, dict_list: list[dict]) -> list[dict]:
        raise NotImplementedError

    def _get(self, dt=datetime.timedelta(days=1)) -> list[dict]:
        raise NotImplementedError
    # def is_registered(self, file_name):
    #     raise NotImplementedError
    #
    # def mark_as_success(self, file_name):
    #     raise NotImplementedError
    #
    # def mark_as_fail(self, file_name):
    #     raise NotImplementedError
    #
    # def get_unfinished(self):
    #     raise NotImplementedError
    #
    # def increment_tries(self, file_name):
    #     raise NotImplementedError
    #
    # def count_tries(self, file_name):
    #     raise NotImplementedError


class LocalBookKeeper(BookKeeper):
    def __init__(self, file_name):
        self.file_name = file_name
        self.df = self._get_df()

    def _get_df(self):
        try:
            return pd.read_csv(self.file_name, sep=',', index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=Task.get_field_names())
            return df

    def update(self, tasks):
        list_ = [t.__dict__ for t in tasks]
        df_ = pd.DataFrame(list_)
        print(df_)

    def add(self, tasks):
        list_ = [t.__dict__ for t in tasks]
        df_ = pd.DataFrame(list_)
        self.df = pd.concat([self.df, df_])

    def get(self, dt=datetime.timedelta(days=1)):
        cutoff = datetime.datetime.now() - dt
        print(f'cutoff = {cutoff}')
        print(f"self.df['created'] = {self.df['created']}")
        x = self.df[self.df['created'] > cutoff]
        return x

    #
    # def register(self, file_name):
    #     self.df.loc[file_name] = {'n_tries': 0, 'status': 'waiting'}
    #
    # def is_registered(self, file_name):
    #     return file_name in self.status_dict
    #
    # def mark_as_success(self, file_name):
    #     self.status_dict[file_name] = 'success'
    #
    # def mark_as_fail(self, file_name):
    #     self.status_dict[file_name] = 'fail'
    #
    # def increment_tries(self, file_name):
    #     self.n_tries_dict[file_name] += 1
    #
    # def get_tries(self, file_name):
    #     return self.n_tries_dict[file_name]
    #
    # def get_unfinished(self):
    #     unfinished = []
    #     for k, v in self.status_dict.items():
    #         if k in ['finished']:
    #             continue
    #         unfinished.append(k)
    #     return unfinished
    #


# TODO: replace this with a DB & REST API
class DBBookKeeper(BookKeeper):
    def __init__(self):
        raise NotImplementedError


book_keepers = {'local': LocalBookKeeper, 'DB': DBBookKeeper}
