import subprocess
import random
import os
import socket
import argparse
import logging
import json
import time
import multiprocessing as mp
from dataclasses import dataclass


@dataclass
class Job:
    """
    not to confuse with task, but job.task_id == task.id
    """
    command: str
    task_id: int


def launch_job(command: str, log_level=logging.INFO) -> None:
    logging.getLogger().setLevel(log_level)
    proc = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = proc.communicate()
    if proc.returncode == 0:
        logging.info(f'successfully ran command <{command}>. stdout:\n{out.decode()}')
    else:
        logging.error(f'error when running command <{command}>. stdout:\n{out.decode()}\nstderr:\n{err.decode()}')


class JobManager:
    def __init__(self, manager, max_processes=8):
        self.q = manager.Queue()
        self.restart_q = manager.Queue()
        self.running_jobs = manager.list()
        self.n_running = max_processes
        self.max_processes = max_processes
        self.pool = [mp.Process(target=self.worker, args=(logging.root.level,)) for _ in range(max_processes)]
        for p in self.pool:
            p.start()

    def worker(self, log_level: int):
        while True:
            job = self.q.get()
            if job is None:  # None means shutdown
                break
            logging.info(f'Process {os.getpid()} working on task {job}')
            launch_job(job.command, log_level)
            logging.info(f'Process {os.getpid()} finished job {job}')
            self.running_jobs.remove(job)
        _ = self.restart_q.get()
        self.worker()

    def enqueue_job(self, command: str, task_id: int) -> str:
        job = Job(command, task_id)
        self.running_jobs.append(job)
        self.q.put(job)
        return f'Job started for task id {task_id}'

    def get_running_task_ids(self) -> list[int]:
        return [job.task_id for job in self.running_jobs]

    def increase_quota(self) -> bool:
        if self.n_running >= self.max_processes:
            return False
        self.restart_q.put(None)
        self.n_running += 1
        return True

    def decrease_quota(self) -> bool:
        if self.n_running == 0:
            return False
        self.q.put(None)
        self.n_running -= 1
        return True

    def change_quota(self, diff: int) -> str:
        if diff > 0:
            for i in range(abs(diff)):
                if not self.increase_quota():
                    return f'Reached max quota ({self.max_processes}) after increasing by {i}'
            return f'Increased quota by {diff}'
        if diff < 0:
            for i in range(abs(diff)):
                if not self.increase_quota():
                    return f'Reached 0 quota after decreasing by {i}'
        return f'Did not change quota (diff=0)'


def process_command(words, jm):
    if words[0] == 'SUBMIT':
        return jm.enqueue_job(words[1], words[2])
    elif words[0] == 'GET_RUNNING':
        return jm.get_running_task_ids()
    elif words[0] == 'CHANGE_QUOTA':
        return jm.change_quota(words[1])
    else:
        return 'invalid command'


def serve_socket(s: socket.socket, jm: JobManager) -> None:
    conn, addr = s.accept()
    with conn:
        logging.info(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                logging.info(f'Received: {data}')
                resp = process_command(json.loads(data.decode()), jm)
                logging.info(f'Returning: {resp}')
                conn.sendall(json.dumps(resp).encode())


def main(args):
    logging.getLogger().setLevel(args.log_level)
    with mp.Manager() as manager:
        job_manager = JobManager(manager, max_processes=1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f'running server under {args.hostname}:{args.port}')
            s.bind((args.hostname, args.port))
            s.listen()
            while True:
                serve_socket(s, job_manager)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=12345)
    parser.add_argument('--max-processes', type=int, default=8)
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    main(parser.parse_args())
