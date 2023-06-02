import subprocess
import random
import socket
import multiprocessing as mp


running_jobs = {}


def simulate_htcondor_job(job):
    # Simulate job running with a subprocess call
    proc = subprocess.Popen(
        # f'echo {job} && sleep {random.randint(1, 5)}',
        f'echo {job} && sleep {2}',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    stdout, stderr = proc.communicate()
    # Register.running_jobs.remove(job)

    if proc.returncode == 0:
        print(f'[stdout]\n{stdout.decode()}')
    else:
        print(f'[stderr]\n{stderr.decode()}')


def start_job(job):
    # Add the job to the Pool
    pool.apply_async(simulate_htcondor_job, (job,))


def run_server():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to a specific address
        s.bind(('localhost', 12345))

        # Listen for incoming connections
        s.listen()

        while True:
            # Accept a connection
            conn, addr = s.accept()

            with conn:
                print(f'Connected by {addr}')
                while True:
                    # Receive a job request
                    job = conn.recv(1024)
                    if not job:
                        break
                    print(f'Received job: {job.decode()}')
                    job = job.decode()
                    if job.startswith('submit'):
                        # Start the job asynchronously
                        result = pool.apply_async(simulate_htcondor_job, (job,))
                        running_jobs[job] = result
                        conn.sendall('Job started'.encode())

                    elif job.startswith('count'):
                        l = []
                        for j, r in running_jobs.items():
                            if not r.ready():
                                l.append(j)
                        conn.sendall(str(l).encode())

                    else:
                        conn.sendall('invalid command'.encode())


if __name__ == '__main__':
    # Create a global Pool with 4 worker processes
    pool = mp.Pool(4)
    run_server()
