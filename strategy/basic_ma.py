from pprint import pprint

class basic_ma_strategy:
    def __init__(self, reader):
        self.reader = reader;

    def execute(self):
        pprint('Strategy started...')
        pprint(self.reader.execute())




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
