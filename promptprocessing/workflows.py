import logging
from promptprocessing import Task


def register_new_files(file_handler, book_keeper):
    new_tasks = []
    registered_files = [t.input for t in book_keeper.get()]
    for f in file_handler.get_files_in_buffer():
        if f not in registered_files:
            logging.info(f'registering new file {f}...')
            t = Task(f, file_handler.get_output_dir(f), f'python analyze.py {f}')
            new_tasks.append(t)
    book_keeper.add(new_tasks)

# def register_new_tasks(file_handler, book_keeper, task_template):
#     pass


def manage_job_queue(file_handler, book_keeper, batch_handler, max_tries=3):
    # running_jobs = batch_handler.get_running()
    running_ids = batch_handler.get_running_ids()
    unfinished_tasks = book_keeper.get_unfinished()
    for t in unfinished_tasks:
        if t.id in running_ids:
            continue
        if file_handler.was_success(t.output):
            t.status = 'success'
            continue
        t.n_tries += 1
        if t.n_tries > t.max_tries:
            t.status = 'fail'
        else:
            batch_handler.submit(t)
    book_keeper.update(unfinished_tasks)


def adjust_batch_quota(book_keeper, batch_handler, goal=10):
    n_unfinished = len(book_keeper.get_unfinished())
    if n_unfinished > goal:
        logging.info('backlog too large, increasing batch quota...')
        batch_handler.increase_quota()
    elif n_unfinished < goal:
        logging.info('backlog too small, decreasing batch quota...')
        batch_handler.decrease_quota()
