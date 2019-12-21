from pprint import pprint


class basic_ma_strategy:
    # data save temp object
    data_storage = {}
    def __init__(self, *args, **kwargs):
        self.reader = kwargs['reader'] if kwargs['reader'] else None
        self.trader = kwargs['trader'] if kwargs['trader'] else None
        self.indicators = kwargs['indicators'] if kwargs['indicators'] else None
        self.adapter = kwargs['adapter'] if kwargs['adapter'] else None

    def _daily_walk(self, *args, **kwargs):
        # daily data walker for checking trading timing
        data = kwargs['row']
        short_ma = list(filter(lambda o: o['date'], self.data_storage['3ma']))[0]
        long_ma = list(filter(lambda o: o['date'], self.data_storage['10ma']))[0]

        # buy condition
        if short_ma['value'] > long_ma['value'] and short_ma['trend_up']:
            self.trader.buy(amount=1, price=data['close'])

        # sell condition
        if long_ma['value'] > short_ma['value'] and short_ma['trend_down']:
            self.trader.sell(amount=1, price=data['close'])

        # stop profit condition
        if self.trader.should_stop_profit():
            self.trader.sell(price=data['close'])

        # stop loss condition
        if self.trader.should_stop_loss():
            self.trader.sell(price=data['close'])


    def _save_raw_data(self, *args, **kwargs):
        if 'raw' not in self.data_storage.keys():
            self.data_storage['raw'] = []

        self.data_storage['raw'] = kwargs['data']

    def execute(self):
        rawdata = list(map(self.adapter.transform, self.reader.get_date_list()))
        self._save_raw_data(data=rawdata)

        for indicator in self.indicators:
            if type(indicator).__name__ is 'simple_moving_average':
                # short ma and long ma
                for count in [3, 10]:
                    key = '%dma' % (count)
                    if key not in self.data_storage.keys():
                        self.data_storage[key] = []
                    self.data_storage[key] = indicator.run(count=count, source=self.data_storage['raw'])

        for row in rawdata:
            self._daily_walk(row=row)

