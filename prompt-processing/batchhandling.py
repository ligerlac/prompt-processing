import abc
import subprocess
# import htcondor
import threading


class BatchHandler(abc.ABC):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


class SubprocessHandler(BatchHandler):
    def __init__(self):
        self.threads = []

    def submit(self, f):
        process = subprocess.Popen('echo "dingeling"', stdout=subprocess.PIPE)
        # subprocess.call('python analyze.py')

    def get_running(self):
        return bool(self.threads)


class HTCondorHandler(BatchHandler):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


class SlurmHandler(BatchHandler):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


batch_handlers = {'HTCondor': HTCondorHandler, 'SlurmHandler': SlurmHandler}
