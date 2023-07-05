import time
import argparse
import logging
import yaml
import promptprocessing as pp


def get_subclass_instance(base_class, config_dict):
    sub_class_dict = {c.__name__: c for c in base_class.__subclasses__()}
    (class_name, sub_dict), = config_dict.items()
    return sub_class_dict[class_name](**sub_dict)


def main(args):
    logging.getLogger().setLevel(args.log_level)

    with open(args.config) as f:
        conf_dict = yaml.safe_load(f)

    batch_handler = get_subclass_instance(pp.BatchHandler, conf_dict['batch_handler'])
    book_keeper = get_subclass_instance(pp.BookKeeper, conf_dict['book_keeper'])
    file_handler = get_subclass_instance(pp.FileHandler, conf_dict['file_handler'])

    if args.workflow == 'register-new-files':
        pp.register_new_files(file_handler, book_keeper)
    elif args.workflow == 'manage-job-queue':
        pp.manage_job_queue(file_handler, book_keeper, batch_handler)
    elif args.workflow == 'adjust-batch-quota':
        pp.adjust_batch_quota(book_keeper, batch_handler)

    while True:
        pp.register_new_files(file_handler, book_keeper)
        pp.manage_job_queue(file_handler, book_keeper, batch_handler)
        pp.adjust_batch_quota(book_keeper, batch_handler)
        time.sleep(args.sleep_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config/local.yaml',
                        help='path to config file')
    parser.add_argument('--workflow', choices=['register-new-files', 'manage-job-queue',
                                               'adjust-batch-quota', 'loop-all'], default='loop-all')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING'],
                        default='WARNING')
    main(parser.parse_args())
