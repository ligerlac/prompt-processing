import time
import argparse
import logging
# from task import Task
from batchhandling import batch_handlers
from bookkeeping import book_keepers
from filehandling import file_handlers


def register_new_files(file_handler, book_keeper):
    for f in file_handler.get_files_in_buffer():
        if not book_keeper.is_registered(f):
            logging.info(f'registering new file {f}...')
            book_keeper.register(f)


def regulate_backlog(book_keeper, batch_handler, goal=10):
    n_unfinished = len(book_keeper.get_unfinished())
    if n_unfinished > goal:
        logging.info('backlog too large, increasing batch quota...')
        batch_handler.increase_quota()
    elif n_unfinished < goal:
        logging.info('backlog too small, decreasing batch quota...')
        batch_handler.decrease_quota()


def process_tasks(file_handler, book_keeper, batch_handler, max_tries=3):
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


class Automation:
    def __init__(self, batch_handler, book_keeper, file_handler, max_tries=3):
        self.batch_handler = batch_handler
        self.book_keeper = book_keeper
        self.file_handler = file_handler
        self.command = 'python scripts/analyze.py {f}'
        self.max_tries = max_tries
        self.last_jobs = []

    def launch_job(self, f):
        logging.info(f'submitting <{self.command.format(f=f)}>')
        self.batch_handler.submit(self.command.format(f=f))
        self.last_jobs.append(f)

    def get_new_files(self):
        new_files = []
        for f in self.file_handler.get_files_in_buffer():
            if not self.book_keeper.is_registered(f):
                new_files.append(f)
        print(f'new_files = {new_files}')
        return new_files

    def process_new_files(self):
        for f in self.get_new_files():
            self.book_keeper.register(f)
            self.launch_job(f)

    def process_failed_job(self, f):
        self.book_keeper.increment_tries(f)
        n_fails = self.book_keeper.get_tries(f)
        logging.info(f'{f} has failed for {n_fails}-th time')
        if n_fails < self.max_tries:
            logging.info(f'{f} try again')
            self.launch_job(f)
        else:
            logging.info(f'{f} exceeded maximum tries {self.max_tries}')
            self.book_keeper.mark_as_fail(f)

    def process_finished_job(self, f):
        self.last_jobs.remove(f)
        if self.file_handler.was_success(f):
            logging.info(f'{f} was successful')
            self.book_keeper.mark_as_success(f)
        else:
            logging.info(f'{f} has failed')
            self.process_failed_job(f)

    def run(self):
        self.process_new_files()
        running_jobs = self.batch_handler.get_running()
        for f in self.last_jobs.copy():
            if f in running_jobs:
                logging.info(f'{f} is still running')
                continue
            logging.info(f'{f} has finished')
            self.process_finished_job(f)


def main(args):
    logging.getLogger().setLevel(args.log_level)

    batch_handler = batch_handlers[args.batch_handler]()
    book_keeper = book_keepers[args.book_keeper]()
    file_handler = file_handlers[args.file_handler]()

    automation = Automation(batch_handler, book_keeper, file_handler)

    while True:
        automation.run()
        time.sleep(args.sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-tries', type=int, default=2)
    parser.add_argument('--sleep-time', type=int, default=10)
    parser.add_argument('--batch-handler', choices=['Socket', 'HTCondor', 'slurm'],
                        default='Socket')
    parser.add_argument('--book-keeper', choices=['local', 'DB'],
                        default='local')
    parser.add_argument('--file-handler', choices=['local'], default='local')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    main(parser.parse_args())
