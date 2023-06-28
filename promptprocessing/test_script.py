from multiprocessing import Process, Queue
import time
import os


def worker(q, fallback_q):
    while True:
        task = q.get()
        if task is None:  # None means shutdown
            break
        print(f'Process {os.getpid()} working on task {task}')
        time.sleep(1)  # Simulate work with time.sleep
        print(f'Process {os.getpid()} finished task {task}')
    _ = fallback_q.get()
    worker(q, fallback_q)


def add_task(q, task):
    q.put(task)


def main():
    q = Queue(maxsize=10)
    fallback_q = Queue(maxsize=10)

    pool = [Process(target=worker, args=(q, fallback_q)) for _ in range(2)]
    for p in pool:
        p.start()

    for i in range(10):
        add_task(q, i)

    q.put(None)

    for i in range(10):
        add_task(q, i)

    fallback_q.put(None)

    for i in range(10):
        add_task(q, i)

    for p in pool:
        p.join()


if __name__ == "__main__":
    main()
