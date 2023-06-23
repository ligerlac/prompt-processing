import abc
import glob
import os


class FileHandler(abc.ABC):

    @staticmethod
    def get_files_in_buffer():
        raise NotImplemented

    @staticmethod
    def was_success(filename):
        raise NotImplemented


class LocalFileHandler(FileHandler):

    @staticmethod
    def get_files_in_buffer():
        return glob.glob('data/input/*')

    @staticmethod
    def was_success(filename):
        filename_ = filename.replace('input', 'output')
        return os.path.isfile(filename_)


file_handlers = {'local': LocalFileHandler}
