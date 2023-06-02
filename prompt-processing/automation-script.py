import time
import argparse
import logging
from batchhandling import batch_handlers
from bookkeeping import book_keepers
from filehandling import get_files_in_buffer, was_success
from dataclasses import dataclass


@dataclass
class Job:
    file_name: str
    pid: int = -1
    n_tries: int = 0
    status: str = 'new'  # [new, running, failed, finished]


def main(args):
    logging.getLogger().setLevel(args.log_level)
    batch_handler = batch_handlers[args.batch_name]()
    book_keeper = book_keepers[args.book_keeper]()

    while True:
        for f in get_files_in_buffer():
            if book_keeper.knows_file(f):
                continue
            j = Job(f)
            book_keeper.register(j)
            batch_handler.submit(j)

        previous_jobs = book_keeper.get_unfinished()
        running_jobs = batch_handler.get_running()

        for f in previous_jobs:
            if f in running_jobs:
                logging.info(f'{f} is still running')
                continue
            logging.info(f'{f} has finished')
            if was_success(f):
                logging.info(f'{f} was successful')
                book_keeper.mark_as_success(f)
                continue
            book_keeper.count_fail(f)
            n_fails = book_keeper.get_n_tries(f)
            logging.info(f'{f} has failed for {n_fails}-th time')
            if n_fails <= args.max_tries:
                logging.info(f'{f} try again')
                batch_handler.submit(f)
            else:
                logging.info(f'{f} exceeded maximum tries {args.max_tries}')
                book_keeper.mark_as_failed(f)

        time.sleep(args.sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-tries', type=int, default=2)
    parser.add_argument('--sleep-time', type=int, default=10)
    parser.add_argument('--batch-name', choices=['HTCondor', 'slurm'],
                        default='HTCondor')
    parser.add_argument('--book-keeper', choices=['local', 'DB'],
                        default='local')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    main(parser.parse_args())
