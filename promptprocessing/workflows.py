import logging


def register_new_files(file_handler, book_keeper):
    for f in file_handler.get_files_in_buffer():
        if not book_keeper.is_registered(f):
            logging.info(f'registering new file {f}...')
            book_keeper.register(f)


def manage_job_queue(file_handler, book_keeper, batch_handler, max_tries=3):
    running_jobs = batch_handler.get_running()
    for f in book_keeper.get_unfinished():
        if f in running_jobs:
            continue
        if file_handler.was_success(f):
            book_keeper.mark_as_success(f)
            continue
        book_keeper.increment_tries(f)
        if book_keeper.get_tries(f) > max_tries:
            book_keeper.mark_as_fail(f)
        else:
            batch_handler.submit(f'python scripts/analyze.py {f}')


def adjust_batch_quota(book_keeper, batch_handler, goal=10):
    n_unfinished = len(book_keeper.get_unfinished())
    if n_unfinished > goal:
        logging.info('backlog too large, increasing batch quota...')
        batch_handler.increase_quota()
    elif n_unfinished < goal:
        logging.info('backlog too small, decreasing batch quota...')
        batch_handler.decrease_quota()
