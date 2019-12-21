from pprint import pprint
from functools import reduce

class simple_moving_average:

    def run(self, *arg, **kwargs):
        count = kwargs['count']
        source = kwargs['source']
        data = []

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
            data.append(d)

        return data