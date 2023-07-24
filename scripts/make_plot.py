import time
import matplotlib.pyplot as plt
import pandas as pd
import argparse


def main(args):
    log_path = 'data/log/metrics.csv'
    df = pd.read_csv(log_path, parse_dates=['ts'], index_col=0)
    # fig, axs = plt.subplots(nrows=3, sharex=True)
    # df.plot(ax=axs[0], y=['files_in_buffer'], ylim=(0, 10))
    # df.plot(ax=axs[1], y=['unfinished_tasks', 'batch_quota', 'running_jobs'])
    # df.plot(ax=axs[2], y=['unfinished_tasks', 'fail_tasks', 'success_tasks'])
    # plt.show()
    fig, axs = plt.subplots(nrows=2, sharex=True)
    # df.plot(ax=axs[0], y=['files_in_buffer'])
    df.plot(ax=axs[0], y=['unfinished_tasks', 'batch_quota'])
    df.plot(ax=axs[1], y=['fail_tasks', 'success_tasks'])
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config/local.yaml',
                        help='path to config file')
    parser.add_argument('--workflow', choices=['register-new-files', 'manage-job-queue',
                                               'adjust-batch-quota', 'loop-all', 'monitor'], default='loop-all')
    main(parser.parse_args())
