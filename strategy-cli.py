from argparse import ArgumentParser

from adapter.twse import adapter
from indicators.simple_moving_average import simple_moving_average
from repository.local_file import repository
from strategy.basic_ma import basic_ma_strategy
from trader.emulator import emulator


def parse_argunments():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target', help='action target')
    arguments = parser.parse_args()

    return {
        'target': arguments.target if arguments.target else None,
    }


def main():
    args = parse_argunments()
    if args['target'] is None:
        raise IOError('target is required')

    data_source = repository(args['target'])
    emulate_trader = emulator(args['target'], cash=1000000)
    strategy_instance = basic_ma_strategy(repository=data_source, trader=emulate_trader, adapter=adapter(),
                                          indicators=[simple_moving_average()])
    strategy_instance.execute()


if __name__ == '__main__':
    main()
