from pprint import pprint
from functools import reduce

class basic_ma_strategy:
    ''' data save temp object '''
    data_storage = {}
    def __init__(self, *args, **kwargs):
        self.reader = kwargs['reader'] if kwargs['reader'] else None
        self.trader = kwargs['trader'] if kwargs['trader'] else None
        self.adapter = kwargs['adapter'] if kwargs['adapter'] else None

    def _save_ma(self, *args, **kwargs):
        ''' moving average '''
        count = kwargs['count']

        key = '%dma' % (count)
        if key not in self.data_storage.keys():
            self.data_storage[key] = []

        target = self.data_storage[key]

        source = self.data_storage['raw']
        for index, row in enumerate(source):
            from_index = index - count if index - count > 0 else 0
            to_index = index

            if to_index - from_index < count:
                continue

            new_source = [item for item in source[from_index:to_index]]

            def sum(accumerlator, row):
                return accumerlator + float(row['close'])

            d = {
                'date': row['date'],
                'value': reduce(sum, new_source, 0) / count,
                'trend_up': new_source[-1]['close'] > new_source[0]['close'],
                'trend_down': new_source[-1]['close'] <= new_source[0]['close'],
            }
            target.append(d)


    def _daily_walk(self, *args, **kwargs):
        ''' daily data walker for checking trading timing '''
        data = kwargs['row']
        short_ma = list(filter(lambda o: o['date'], self.data_storage['3ma']))[0]
        long_ma = list(filter(lambda o: o['date'], self.data_storage['10ma']))[0]

        ''' buy condition '''
        pprint('date: %s, buy: %s' % (data['date'], short_ma['value'] > long_ma['value'] and short_ma['trend_up']))
        if short_ma['value'] > long_ma['value'] and short_ma['trend_up']:
            self.trader.buy(amount=1, prize=data['close'])

        ''' sell condition '''
        if long_ma['value'] > short_ma['value'] and short_ma['trend_down']:
            self.trader.sell(amount=1, prize=data['close'])

        ''' stop profit condition '''
        if self.trader.should_stop_profit():
            self.trader.sell(amount=1, prize=data['close'])

        ''' stop loss condiition '''
        if self.trader.should_stop_loss():
            self.trader.sell(amount=1, prize=data['close'])


    def _save_raw_data(self, *args, **kwargs):
        if 'raw' not in self.data_storage.keys():
            self.data_storage['raw'] = []

        self.data_storage['raw'] = kwargs['data']

    def execute(self):
        rawdata = list(map(self.adapter.transform, self.reader.get_date_list()))
        self._save_raw_data(data=rawdata)

        self._save_ma(count=3)
        self._save_ma(count=10)

        for row in rawdata:
            self._daily_walk(row=row)

    def trade(self, *args, **kwargs):
        ''' trad function '''







# def parse_argunments():
#     parser = ArgumentParser()
#     parser.add_argument('-s', '--start', help='crawl from specific date')
#     parser.add_argument('-e', '--end', help='crawl to specific date, default is today')
#     parser.add_argument('--strategy', help='run strategy')
#     parser.add_argument('--target', help='target')
#     arguments = parser.parse_args()
#     return {
#         'start': datetime.strptime(arguments.start, '%Y-%m-%d') or None,
#         'end': datetime.strptime(arguments.end, '%Y-%m-%d') or None,
#         'strategy': arguments.strategy or None,
#         'target': arguments.target or None,
#     }
#
#
# def main():
#     args = parse_argunments()
#
#     if args.target is None:
#         raise IOError('target is required')
#
#     data_source = reader('0050')
#     data_source.execute(start=args['start'], end=args['end'])
#
#
# if __name__ == '__main__':
#     main()
