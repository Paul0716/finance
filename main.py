from argparse import ArgumentParser
from datetime import datetime
from stock_report.crawler import crawler
from stock_report.reader import reader
from stock_report.trader import trader
from stock_report.adapter import adapter
from strategy.basic_ma import basic_ma_strategy
from indicators.simple_moving_average import simple_moving_average
from pprint import pprint

def parse_argunments():
    parser = ArgumentParser()
    parser.add_argument('-s', '--start', help='crawl from specific date')
    parser.add_argument('-e', '--end', help='crawl to specific date, default is today')
    parser.add_argument('-b','--back', help='crawl specific date')
    parser.add_argument('-t', '--target', help='action target')
    parser.add_argument('--strategy', help='run strategy')
    arguments = parser.parse_args()

    return {
        'start': datetime.strptime(arguments.start, '%Y-%m-%d') if arguments.start else None,
        'end': datetime.strptime(arguments.end, '%Y-%m-%d') if arguments.end else None,
        'back': int(arguments.back) if arguments.back else None,
        'target': arguments.target if arguments.target else None,
        'strategy': arguments.strategy if arguments.strategy else None,
    }

def main():
    args = parse_argunments()
    if args['target'] is None:
        raise IOError('target is required')

    data_source = reader(args['target'])
    emulate_trader = trader(args['target'], cash=1000000)


    if args['strategy'] is None:
        stock_crawler = crawler(args['target'])
        stock_crawler.execute(start=args['start'], end=args['end'])
    else:
        strategy_instance = basic_ma_strategy(reader=data_source, trader=emulate_trader, adapter=adapter(), indicators=[simple_moving_average()])
        strategy_instance.execute()

if __name__ == '__main__':
    main()