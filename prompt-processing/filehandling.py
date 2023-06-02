import glob
import random


def get_files_in_buffer():
    return glob.glob('data/*')


def was_success(f):
    return random.random() > 0.5
