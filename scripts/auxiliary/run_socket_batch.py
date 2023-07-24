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


def launch_job(command: str, log_level: int = logging.INFO) -> None:
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


def worker(q, restart_q, wait_bool,running_jobs, log_level: int):
    while True:
        job = q.get()
        if job is None:  # None means shutdown
            wait_bool.value = False
            break
        logging.info(f'Process {os.getpid()} working on task {job}')
        launch_job(job.command, log_level)
        logging.info(f'Process {os.getpid()} finished job {job}')
        running_jobs.remove(job)
    print(f'Shutting down worker with id {os.getpid()}')
    _ = restart_q.get()
    print(f'Restarting worker with id {os.getpid()}')
    worker(q, restart_q, wait_bool, running_jobs, log_level)


class JobManager:
    def __init__(self, manager, max_quota=8):
        self.q = manager.Queue()
        self.restart_q = manager.Queue()
        self.running_jobs = manager.list()
        self.waiting_for_shutdown = manager.Value('i', False)
        self.quota = max_quota
        self.max_quota = max_quota
        self.pool = [mp.Process(target=worker, args=(self.q, self.restart_q, self.waiting_for_shutdown,
                                                     self.running_jobs, logging.root.level)
                                     ) for _ in range(max_quota)]
        for p in self.pool:
            p.start()

    # def worker(self, log_level: int):
    #     while True:
    #         job = self.q.get()
    #         if job is None:  # None means shutdown
    #             self.waiting_for_shutdown.value = False
    #             break
    #         logging.info(f'Process {os.getpid()} working on task {job}')
    #         launch_job(job.command, log_level)
    #         logging.info(f'Process {os.getpid()} finished job {job}')
    #         self.running_jobs.remove(job)
    #     _ = self.restart_q.get()
    #     self.worker(log_level)

    def enqueue_job(self, command: str, task_id: int) -> str:
        job = Job(command, task_id)
        self.running_jobs.append(job)
        self.q.put(job)
        return f'Job started for task id {task_id}'

    def get_running_task_ids(self) -> list[int]:
        return [job.task_id for job in self.running_jobs]

    def increase_quota(self) -> bool:
        if self.quota >= self.max_quota:
            return False
        self.restart_q.put(None)
        self.quota += 1
        return True

    def decrease_quota(self) -> bool:
        print(f'decrease_quota(), waiting for shutdown.value = {self.waiting_for_shutdown.value}')
        if self.quota <= 1 or self.waiting_for_shutdown.value:
            return False
        self.waiting_for_shutdown.value = True
        self.q.put(None)
        self.quota -= 1
        return True

    def change_quota(self, diff: int) -> str:
        if diff > 0:
            for i in range(abs(diff)):
                if not self.increase_quota():
                    return f'Reached max quota ({self.max_quota}) after increasing by {i}'
            return f'Increased quota by {diff}'
        if diff < 0:
            for i in range(abs(diff)):
                if not self.decrease_quota():
                    return f'Reached 0 quota after decreasing by {i}'
            return f'Decreased quota by {abs(diff)}'
        return f'Did not change quota (diff=0)'

    def set_quota(self, n) -> str:
        for _ in range(self.quota):
            self.q.put(None)
        m = self.max_quota if (n > self.max_quota) else n
        for _ in range(m):
            self.restart_q.put(None)
        self.quota = m
        return f'Set quota to {m}'


def process_command(words, jm):
    if words[0] == 'SUBMIT':
        return jm.enqueue_job(words[1], words[2])
    elif words[0] == 'GET_RUNNING':
        return jm.get_running_task_ids()
    elif words[0] == 'CHANGE_QUOTA':
        return jm.change_quota(words[1])
    elif words[0] == 'SET_QUOTA':
        return jm.set_quota(words[1])
    elif words[0] == 'GET_QUOTA':
        return jm.quota
    elif words[0] == 'GET_MAX_QUOTA':
        return jm.max_quota
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
    # pool = [mp.Process(target=JobManager.worker, args=(logging.root.level,)) for _ in range(8)]
    logging.getLogger().setLevel(args.log_level)
    with mp.Manager() as manager:
        job_manager = JobManager(manager, max_quota=8)
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
