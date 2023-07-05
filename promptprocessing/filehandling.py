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

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_files_in_buffer(self):
        return glob.glob(f'{self.input_dir}/*')

    def was_success(self, filename):
        # filename_ = filename.replace('input', 'output')
        filename_ = f'{self.output_dir}/{filename}'
        return os.path.isfile(filename_)
