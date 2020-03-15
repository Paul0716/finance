from pprint import pprint

from trader.trade_type import TradeType


class basic_ma_strategy:
    # data save temp object
    data_storage = {}

    def __init__(self, *args, **kwargs):
        self.repository = kwargs['repository'] if kwargs['repository'] else None
        self.trader = kwargs['trader'] if kwargs['trader'] else None
        self.indicators = kwargs['indicators'] if kwargs['indicators'] else None
        self.adapter = kwargs['adapter'] if kwargs['adapter'] else None

    def _daily_walk(self, *args, **kwargs):
        # daily data walker for checking trading timing
        data = kwargs['row']
        condition = self._check_timing(row=data)
        # pprint(data)
        # buy condition
        if condition['buy']:
            self.trader.buy(type=TradeType.All, price=data['close'], date=data['date'])

        # sell condition
        if condition['sell']:
            self.trader.sell(type=TradeType.All, price=data['close'], date=data['date'])

        # stop profit condition
        if self.trader.should_stop_profit():
            self.trader.sell(type=TradeType.All, price=data['close'], date=data['date'])

        # stop loss condition
        if self.trader.should_stop_loss():
            self.trader.sell(type=TradeType.All, price=data['close'], date=data['date'])

    def _check_timing(self, *args, **kwargs):
        def get_moving_average(source):
            return list(filter(lambda o: o['date'] is kwargs['row']['date'], source))

        short = get_moving_average(self.data_storage['5ma'])[0] if (
                len(get_moving_average(self.data_storage['5ma'])) > 0) else None
        long = get_moving_average(self.data_storage['10ma'])[0] if (
                len(get_moving_average(self.data_storage['10ma'])) > 0) else None
        return {
            'buy': short['value'] > long['value'] and short['trend_up'] if short and long else False,
            'sell': long['value'] > short['value'] and short['trend_down'] if short and long else False,
        }

    def _save_raw_data(self, *args, **kwargs):
        if 'raw' not in self.data_storage.keys():
            self.data_storage['raw'] = []

        self.data_storage['raw'] = kwargs['data']

    def execute(self):
        rawdata = list(map(self.adapter.transform, self.repository.read()))
        self._save_raw_data(data=rawdata)
        for indicator in self.indicators:
            if type(indicator).__name__ is 'simple_moving_average':
                # short ma and long ma
                for count in [5, 10]:
                    key = '%dma' % (count)
                    if key not in self.data_storage.keys():
                        self.data_storage[key] = []
                    self.data_storage[key] = indicator.run(count=count, source=self.data_storage['raw'])

        for row in rawdata:
            self._daily_walk(row=row)

        pprint(self.trader.performance_report())
