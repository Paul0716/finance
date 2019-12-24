from abstract.base import base


class adapter(base):

    def to_append_cell(self, row):
        return {
            'values': [
                {
                    'userEnteredValue': {
                        'stringValue': row['date']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['volume']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['amount_of_transaction']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['open']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['high']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['low']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['close']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['spread']
                    }
                },
                {
                    'userEnteredValue': {
                        'stringValue': row['number_of_transactions']
                    }
                },
            ]
        }
