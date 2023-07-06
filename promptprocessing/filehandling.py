import abc
import glob
import os


class FileHandler(abc.ABC):

    @staticmethod
    def get_files_in_buffer():
        raise NotImplementedError

    @staticmethod
    def was_success(filename):
        raise NotImplementedError

    def get_output_dir(self, file_name):
        raise NotImplementedError


class LocalFileHandler(FileHandler):

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def get_files_in_buffer(self):
        return glob.glob(f'{self.input_dir}/*')

    def was_success(self, file_name):
        # filename_ = filename.replace('input', 'output')
        return os.path.isfile(self.get_output_dir(file_name))

    def get_output_dir(self, file_name):
        return f'{self.output_dir}/{file_name}'
