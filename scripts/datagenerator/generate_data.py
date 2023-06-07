#!/usr/bin/env python3

import argparse
import logging
import os
from ROOT import TFile, TTree, gRandom
import time
from array import array


def create_root_file(filename):
    f = TFile(filename, "recreate")

    tree = TTree("T", "test tree")

    x = array('f', [0])
    tree.Branch("X", x, "X/F")

    for i in range(100):
        x[0] = gRandom.Uniform()
        tree.Fill()

    tree.Write()
    f.Close()


def main(args):
    logging.getLogger().setLevel(args.log_level)
    logging.info(f'output will be written to {args.output}')
    os.makedirs(args.output, exist_ok=True)
    while True:
        timestamp = int(time.time())
        filename = os.path.join(args.output, f'file_{timestamp}.root')
        create_root_file(filename)
        logging.info(f'wrote file {filename}')
        logging.info(f'sleeping for {args.period}s')
        time.sleep(args.period)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='data')
    parser.add_argument('--period', type=int, default=10)
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    main(parser.parse_args())
