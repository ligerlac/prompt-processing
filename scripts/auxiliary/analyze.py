import argparse
import random
import os
import time
import numpy as np
from pathlib import Path


def main(args):
    print(f'analyzing file {args.filename}')
    if not os.path.isfile(args.filename):
        raise FileNotFoundError(f'no file named {args.filename}')
    success = (random.uniform(0, 1) <= args.success_rate)
    print(f'success = {success}')
    if success:
        out_name = args.filename.split('/')[-1].replace('.', '_processed.')
        print(f'out_name = {args.output}/{out_name}')
        Path(f'{args.output}/{out_name}').touch()
    time.sleep(np.random.chisquare(args.sleep_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument('--output', type=str, default='data/output/')
    parser.add_argument('--success-rate', type=float, default=1.0)
    parser.add_argument('--sleep-time', type=float, default=10)
    main(parser.parse_args())
