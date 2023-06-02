import subprocess
import random
import socket
import multiprocessing as mp
import argparse
import logging


all_jobs = {}


def launch_job(job: str, log_level: int) -> None:
    logging.getLogger().setLevel(log_level)
    proc = subprocess.Popen(
        # f'echo {job} && sleep {random.randint(1, 5)}',
        f'echo {job} && sleep {2}', shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode == 0:
        logging.info(f'job {job} returned {out.decode()}')
    else:
        logging.error(err.decode())


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
    return {'submit': enqueue_job(first_word),
            'count': get_running_jobs()
            }.get(first_word, 'invalid command')


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
