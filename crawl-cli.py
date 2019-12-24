from argparse import ArgumentParser
from datetime import datetime

from adapter.twse import adapter
from crawler.twse import crawler
from repository.local_file import repository


def parse_argunments():
    parser = ArgumentParser()
    parser.add_argument('-s', '--start', help='crawl from specific date')
    parser.add_argument('-e', '--end', help='crawl to specific date, default is today')
    parser.add_argument('-t', '--target', help='action target')
    arguments = parser.parse_args()

    return {
        'start': datetime.strptime(arguments.start, '%Y-%m-%d') if arguments.start else None,
        'end': datetime.strptime(arguments.end, '%Y-%m-%d') if arguments.end else None,
        'target': arguments.target if arguments.target else None,
    }


def transform(*args, **kwargs):
    twse_adapter = adapter()
    return twse_adapter.transform_to_source(twse_adapter.transform_from_source(kwargs['row']))


def main():
    args = parse_argunments()
    if args['target'] is None:
        raise IOError('target is required')

    stock_crawler = crawler(args['target'], repository=repository(args['target']))
    stock_crawler.execute(start=args['start'], end=args['end'], walker=transform)


if __name__ == '__main__':
    main()
