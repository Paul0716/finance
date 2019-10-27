from argparse import ArgumentParser
from pprint import pprint
from datetime import datetime
from stock_report import crawler

def parse_argunments():
    parser = ArgumentParser()
    parser.add_argument('-s', '--start', help='crawl from specific date')
    parser.add_argument('-e', '--end', help='crawl to specific date, default is today')
    parser.add_argument('-b','--back', help='crawl specific date')

    parser.print_help()
    arguments = parser.parse_args()
    return {
        'start': datetime.strptime(arguments.start, '%Y-%m-%d') or None,
        'end': datetime.strptime(arguments.start, '%Y-%m-%d') or None,
        'back': int(arguments.back) if arguments.back else None,
    }

def main():
    args = parse_argunments()
    crawler.execute()


if __name__ == '__main__':
    main()