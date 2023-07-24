import logging
import time
import csv, os
import random
from datetime import datetime
from promptprocessing import Task


def register_new_files(file_handler, book_keeper):
    new_tasks = []
    registered_files = [t.input for t in book_keeper.get()]
    for f in file_handler.get_files_in_buffer():
        if f not in registered_files:
            logging.info(f'registering new file {f}...')
            t = Task(f, f.replace('.', '_processed.').replace('/input/', '/output/'),
                     f'python scripts/auxiliary/analyze.py {f}'
                     # f' --success-rate 1.0 --sleep-time 8')
                     # f' --success-rate 0.5 --sleep-time 8')  # at 2:16
                     f' --success-rate 0.0 --sleep-time 8')  # at 2:20
                     # f' --success-rate 1.0 --sleep-time 4')
            new_tasks.append(t)
    book_keeper.add(new_tasks)


# def register_new_tasks(file_handler, book_keeper, task_template):
#     pass


def manage_job_queue(file_handler, book_keeper, batch_handler, max_tries=3):
    # running_jobs = batch_handler.get_running()
    running_ids = batch_handler.get_running_ids()
    unfinished_tasks = book_keeper.get(status='unfinished')
    for t in unfinished_tasks:
        if t.id in running_ids:
            continue
        if file_handler.was_success(t.output):
            logging.info(f'found {t.output}, mark task as success...')
            t.status = 'success'
            continue
        logging.info(f'did not find {t.output}, retry')
        if t.n_tries >= t.max_tries:
            t.status = 'fail'
        else:
            batch_handler.submit(t)
            t.n_tries += 1
    book_keeper.update(unfinished_tasks)


def adjust_batch_quota(book_keeper, batch_handler, goal=8):
    n_unfinished = len(book_keeper.get(status='unfinished'))
    # if n_unfinished > goal:
    #     logging.info('backlog too large, increasing batch quota...')
    #     batch_handler.increase_quota()
    # elif n_unfinished < goal:
    #     logging.info('backlog too small, decreasing batch quota...')
    #     batch_handler.decrease_quota()
    logging.info(f'backlog: {n_unfinished}, goal: {goal}')
    if random.random() > abs((n_unfinished-goal)/goal):
        logging.info('randomly chose not to change quota...')
        return
    if n_unfinished > goal:
        logging.info('backlog too large, increasing batch quota...')
        batch_handler.increase_quota()
    elif n_unfinished < goal:
        logging.info('backlog too small, decreasing batch quota...')
        batch_handler.decrease_quota()


def monitor(file_handler, book_keeper, batch_handler, path='data/log/metrics.csv'):
    while True:
        n = {}
        n['ts'] = datetime.now()
        n['files_in_buffer'] = len(file_handler.get_files_in_buffer())
        n['running_jobs'] = len(batch_handler.get_running_ids())
        n['batch_quota'] = batch_handler.get_quota()
        for status in ['all', 'unfinished', 'fail', 'success']:
            n[f'{status}_tasks'] = 0
        # for t in book_keeper.get(dt=timedelta(seconds=10)):
        for t in book_keeper.get():
            n['all_tasks'] += 1
            n[f'{t.status}_tasks'] += 1

        add_headers = not os.path.isfile(path)
        with open(path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=n.keys())
            if add_headers:
                writer.writeheader()
            writer.writerow(n)
        time.sleep(2)
