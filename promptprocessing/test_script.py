import socket
import time
import subprocess
from batchhandling import SocketBatchHandler
from promptprocessing import Task


handler = SocketBatchHandler()

t = Task('input', 'output', 'python analyze.py')
t2 = Task('input', 'output', 'sleep 2')
setattr(t, '_id', 42)  # to circumvent read-only id
setattr(t2, '_id', 69)  # to circumvent read-only id

handler.submit(t)
handler.submit(t2)
time.sleep(0.1)
print(f'handler.get_running() = {handler.get_running()}')

time.sleep(0.1)
print(f'handler.get_running() = {handler.get_running()}')
time.sleep(0.1)
print(f'handler.get_running() = {handler.get_running()}')



# handler.submit('submit python -c "print(\'from python\')"')
# handler.submit('count')
# time.sleep(3)
# handler.submit('count')


exit(0)


class LocalBatchSimulator:
    def __init__(self, address='localhost', port=12345):
        self.address = address
        self.port = port

    def submit_job(self, job):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.address, self.port))
            s.sendall(job.encode())
            data = s.recv(1024)
        print(f'Received: {data.decode()}')


if __name__ == '__main__':
    simulator = LocalBatchSimulator()
    simulator.submit_job('Job1')
    simulator.submit_job('Job2')
