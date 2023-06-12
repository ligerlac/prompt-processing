import subprocess
import random
import socket
import multiprocessing as mp
import argparse
import logging


all_jobs = {}


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


def enqueue_job(line: str) -> str:
    result = pool.apply_async(launch_job, (line, logging.root.level))
    all_jobs[line] = result
    return 'Job started'


def get_running_jobs() -> str:
    running_jobs = []
    for j, r in all_jobs.items():
        if not r.ready():
            running_jobs.append(j)
    return str(running_jobs)


def process_command(line) -> str:
    first_word = line.split(' ')[0]
    rest = line[len(first_word)+1:]
    if first_word == 'submit':
        return enqueue_job(rest)
    elif first_word == 'count':
        return get_running_jobs()
    else:
        return 'invalid command'


def serve_socket(s: socket.socket()) -> None:
    conn, _ = s.accept()
    request = conn.recv(1024)
    if not request:
        return
    line = request.decode()
    logging.info(f'Received line: {line}')
    resp = process_command(line)
    conn.sendall(resp.encode())


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
