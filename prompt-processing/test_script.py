import socket
from batchhandling import SocketBatchHandler
import time

handler = SocketBatchHandler()
handler.submit_job('submit echo hee hee')
handler.submit_job('submit test')
handler.submit_job('submit python -c "print(\'from python\')"')
handler.submit_job('count')
time.sleep(3)
handler.submit_job('count')


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
