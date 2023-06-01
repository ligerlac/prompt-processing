import glob
import time
import argparse
import logging
import bookkeeping
import yaml


def get_new_files():
    return glob.glob('data/*')


def main(args):
    logging.getLogger().setLevel(args.log_level)

    while True:
        new_files = get_new_files()
        for f in new_files:
            bookkeeping.files_to_process.add(f)
        print(f'files_to_process = {bookkeeping.files_to_process}')
        time.sleep(10)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,
                        default='tests/data/2022-09-12_21-13-47.npy',
                        help='name of input file')
    parser.add_argument('--conf', type=str, default='conf/test/echo_and_add.json',
                        help='name of job config file')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    main(parser.parse_args())
