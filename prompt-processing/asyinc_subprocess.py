import asyncio
import subprocess
import random


class JobTracker:
    def __init__(self):
        self.running_jobs = 0

    def increment(self):
        self.running_jobs += 1

    def decrement(self):
        self.running_jobs -= 1

    def count(self):
        return self.running_jobs


async def simulate_htcondor_job(job, job_tracker):
    job_tracker.increment()

    # Simulate job running with a subprocess call
    proc = await asyncio.create_subprocess_shell(
        f'echo {job} && sleep {random.randint(1, 5)}',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    job_tracker.decrement()

    print(f'[stdout]\n{stdout.decode()}')


async def monitor_jobs(job_tracker):
    while True:
        print(f'Running jobs: {job_tracker.count()}')
        await asyncio.sleep(1)


async def main():
    # Simulated list of jobs
    jobs = ['Job1', 'Job2', 'Job3']

    job_tracker = JobTracker()

    # Create a list of tasks to run in parallel
    job_tasks = [simulate_htcondor_job(job, job_tracker) for job in jobs]

    # Add the monitoring task
    tasks = job_tasks + [monitor_jobs(job_tracker)]

    # Asynchronously run tasks
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
