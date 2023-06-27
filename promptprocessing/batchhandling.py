import abc
# import htcondor
import socket
import pickle
from promptprocessing import Task


class BatchHandler(abc.ABC):
    def submit(self, task: Task):
        raise NotImplementedError

    def get_running(self) -> list[Task]:
        raise NotImplementedError

    def increase_quota(self):
        raise NotImplementedError

    def decrease_quota(self):
        raise NotImplementedError


class SocketBatchHandler(BatchHandler):
    def __init__(self, address='localhost', port=12345):
        self.address = address
        self.port = port

    def send_string(self, content) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.address, self.port))
            s.sendall(content.encode())
            return s.recv(1024).decode()

    def submit(self, task: Task):
        if task.id is None:
            raise RuntimeError('attempted to submit a task without an id. forgot to register it?')
        r = self.send_string(f'SUBMIT|{task.command}|{task.id}')
        print(f'submitted job, resp = {r}')

    def get_running(self) -> list[Task]:
        print('get_running()')
        r = self.send_string('GET_RUNNING')
        print(f'resp = {r}')

    def receive_all(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # s.connect((self.address, self.port))
            # s.bind((self.address, self.port))
            s.listen()
            sock, _ = s.accept()
            data_chunks = []
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                data_chunks.append(chunk)
            return b''.join(data_chunks)


class HTCondorBatchHandler(BatchHandler):
    def submit(self, task: Task):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


class SlurmBatchHandler(BatchHandler):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


batch_handlers = {'HTCondor': HTCondorBatchHandler,
                  'Slurm': SlurmBatchHandler,
                  'Socket': SocketBatchHandler}
