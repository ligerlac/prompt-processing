import subprocess
import random
import socket
import argparse
import logging
import json
import multiprocessing as mp
from dataclasses import dataclass


@dataclass
class Job:
    """
    not to confuse with task, but job.task_id == task.id
    """
    command: str
    task_id: int
    result: None = None


running_jobs = []


def receive_all(sock):
    data_chunks = []
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data_chunks.append(chunk)
    return b''.join(data_chunks)


def launch_job(command: str, log_level: int) -> None:
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


def enqueue_job(command: str, task_id: int) -> str:
    job = Job(command, task_id)
    job.result = pool.apply_async(launch_job, (command, logging.root.level))
    running_jobs.append(job)
    return f'Job started for task id {task_id}'


def get_running_task_ids() -> list[int]:
    print(f'running_jobs = {running_jobs}')
    running_task_ids = []
    for j in running_jobs.copy():
        if j.result.ready():
            running_jobs.remove(j)
        else:
            running_task_ids.append(j.task_id)
    return running_task_ids


def change_quota(diff: int):
    return 'changed'


def process_command(words):
    if words[0] == 'SUBMIT':
        return enqueue_job(words[1], words[2])
    elif words[0] == 'GET_RUNNING':
        return get_running_task_ids()
    elif words[0] == 'CHANGE_QUOTA':
        return change_quota(words[1])
    else:
        return 'invalid command'


def serve_socket(s: socket.socket) -> None:
    conn, addr = s.accept()
    with conn:
        logging.info(f'Connected by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                logging.info(f'Received: {data}')
                resp = process_command(json.loads(data.decode()))
                logging.info(f'Returning: {resp}')
                conn.sendall(json.dumps(resp).encode())


def main(args):
    logging.getLogger().setLevel(args.log_level)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f'running server under {args.hostname}:{args.port}')
        s.bind((args.hostname, args.port))
        s.listen()
        while True:
            serve_socket(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=12345)
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    pool = mp.Pool(4)
    main(parser.parse_args())
