import abc
import datetime
import pandas as pd
from promptprocessing.task import Task


class BookKeeper(abc.ABC):
    """
    keeps a collection of tasks
    """
    def update(self, task_list: list[Task]) -> None:
        raw = {}
        for t in task_list:
            raw[t.id] = t.get_dict_wo_id()
        self._update(raw)

    def add(self, task_list: list[Task]) -> None:
        self._add([t.get_dict_wo_id() for t in task_list])

    def get(self, dt=datetime.timedelta(days=1), status=None) -> list[Task]:
        raw = self._get(dt, status)
        return [Task(**x) for x in raw]

    def _update(self, id_task_dict: dict) -> None:
        raise NotImplementedError

    def _add(self, task_dict_list: list[dict]) -> None:
        raise NotImplementedError

    def _get(self, dt=datetime.timedelta(days=1), status=None) -> list[dict]:
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

    def _write_df(self, df):
        df.to_csv(self.file_name, sep=',')

    def _get_df(self):
        try:
            return pd.read_csv(self.file_name, sep=',', index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=Task.get_field_names())
            return df

    def _update(self, id_task_dict: dict) -> None:
        df = self._get_df()
        for i, d in id_task_dict.items():
            df.iloc[i] = d
        self._write_df(df)

    def _add(self, task_dict_list: list[dict]) -> None:
        df_before = self._get_df()
        new_df = pd.DataFrame(task_dict_list)
        df_after = pd.concat([df_before, new_df], ignore_index=True)
        self._write_df(df_after)

    def _get(self, dt=datetime.timedelta(days=1), status=None) -> list[dict]:
        df = self._get_df()
        cutoff = datetime.datetime.now() - dt
        df_filtered = df[pd.to_datetime(df['created']) > cutoff]
        if status is not None:
            df_filtered = df_filtered[df_filtered['status'] == status]
        records = df_filtered.to_dict(orient='records')
        ids = df_filtered.to_dict(orient='tight')['index']
        for r, i in zip(records, ids):
            r['created'] = pd.to_datetime(r['created'])
            r['_id'] = i
        return records

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
