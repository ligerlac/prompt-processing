import abc
import subprocess
# import htcondor
import threading
import socket


class BatchHandler(abc.ABC):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


class SocketBatchHandler(BatchHandler):
    def __init__(self, address='localhost', port=12345):
        self.address = address
        self.port = port

    def submit_job(self, job):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.address, self.port))
            s.sendall(job.encode())
            data = s.recv(1024)
        print(f'Received: {data.decode()}')

    def get_running(self):
        return self.running_jobs


class HTCondorBatchHandler(BatchHandler):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


class SlurmBatchHandler(BatchHandler):
    def submit(self, f):
        raise NotImplemented

    def get_running(self):
        raise NotImplemented


batch_handlers = {'HTCondor': HTCondorBatchHandler, 'Slurm': SlurmBatchHandler, 'Socket': SocketBatchHandler}
