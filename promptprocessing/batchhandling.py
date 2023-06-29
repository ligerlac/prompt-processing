import abc
# import htcondor
import socket
import json
from promptprocessing.task import Task


class BatchHandler(abc.ABC):
    def submit(self, task: Task):
        raise NotImplementedError

    def get_running_ids(self) -> list[int]:
        raise NotImplementedError

    def increase_quota(self):
        raise NotImplementedError

    def decrease_quota(self):
        raise NotImplementedError

    def get_quota(self):
        raise NotImplementedError

    def set_quota(self, n):
        raise NotImplementedError


class SocketBatchHandler(BatchHandler):
    def __init__(self, address='localhost', port=12345):
        self.address = address
        self.port = port

    def send(self, content):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.address, self.port))
            s.sendall(json.dumps(content).encode())
            data = s.recv(1024)
            return json.loads(data.decode())

    def submit(self, task: Task):
        if task.id is None:
            raise RuntimeError('attempted to submit a task without an id. forgot to register it?')
        self.send(['SUBMIT', task.command, task.id])

    def get_running_ids(self) -> list[int]:
        return self.send(['GET_RUNNING'])

    def increase_quota(self):
        return self.send(['CHANGE_QUOTA', 1])

    def decrease_quota(self):
        return self.send(['CHANGE_QUOTA', -1])

    def get_quota(self):
        return self.send(['GET_QUOTA'])

    def set_quota(self, n):
        return self.send(['SET_QUOTA', n])

    def get_max_quota(self):
        return self.send(['GET_MAX_QUOTA'])


class HTCondorBatchHandler(BatchHandler):
    def submit(self, task: Task):
        raise NotImplementedError

    def get_running_ids(self):
        raise NotImplementedError


class SlurmBatchHandler(BatchHandler):
    def submit(self, f):
        raise NotImplementedError

    def get_running_ids(self):
        raise NotImplementedError


batch_handlers = {'HTCondor': HTCondorBatchHandler,
                  'Slurm': SlurmBatchHandler,
                  'Socket': SocketBatchHandler}
