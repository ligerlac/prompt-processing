import abc
import pandas


class BookKeeper(abc.ABC):
    def register(self, file_name):
        raise NotImplemented

    def knows_file(self, file_name):
        raise NotImplemented

    def get_unfinished(self):
        raise NotImplemented

    def count_fail(self):
        raise NotImplemented


class LocalBookKeeper(BookKeeper):
    def __init__(self):
        self.status_dict = {}
        self.n_tries_dict = {}

    def register(self, file_name):
        self.status_dict[file_name] = 'to_process'
        self.n_tries_dict[file_name] = 0

    def knows_file(self, file_name):
        return file_name in self.status_dict

    def get_unfinished(self):
        unfinished = []
        for k, v in self.status_dict.items():
            if k in ['finished']:
                continue
            unfinished.append(v)
        return unfinished


# TODO: replace this with a DB & REST API
class DBBookKeeper(BookKeeper):
    def __init__(self):
        raise NotImplemented

    def register(self, file_name):
        raise NotImplemented

    def is_registered(self, file_name):
        raise NotImplemented


book_keepers = {'local': LocalBookKeeper, 'DB': DBBookKeeper}
