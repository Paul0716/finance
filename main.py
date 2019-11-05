from argparse import ArgumentParser
from pprint import pprint
from datetime import datetime
# from stock_report import crawler
from stock_report.crawler import crawler

def parse_argunments():
    parser = ArgumentParser()
    parser.add_argument('-s', '--start', help='crawl from specific date')
    parser.add_argument('-e', '--end', help='crawl to specific date, default is today')
    parser.add_argument('-b','--back', help='crawl specific date')
    arguments = parser.parse_args()
    return {
        'start': datetime.strptime(arguments.start, '%Y-%m-%d') or None,
        'end': datetime.strptime(arguments.end, '%Y-%m-%d') or None,
        'back': int(arguments.back) if arguments.back else None,
    }

def main():
    args = parse_argunments()

    stock_crawler = crawler('0050')
    stock_crawler.execute(start=args['start'], end=args['end'])


if __name__ == '__main__':
    main()