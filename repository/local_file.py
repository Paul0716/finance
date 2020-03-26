import csv
import os
class repository:

    def __init__(self, stock_number, *args, **kwargs):
        self.stock_number = stock_number

    def save(self, *args, **kwargs):
        path = self._get_file_path(name=kwargs['name'])
        self._check_if_file_exists(filename=path)
        if type(kwargs["data"]) is list:
            with open(path, 'a') as b:
                for row in kwargs["data"]:
                    writer = csv.writer(b)
                    writer.writerow(row.split(','))
        else:
            with open(path, 'a') as b:
                writer = csv.writer(b)
                writer.writerow(kwargs["data"])

    def read(self, *args, **kwargs):

        def sorted_by_date(item):
            return item[0]

        return sorted(self._read_file(name=self.stock_number), key=sorted_by_date)

    def get_date_list(self, *args, **kwargs):
        return self.read(name=self.stock_number)

    def _read_file(self, *args, **kwargs):
        data_list = []
        path = self._get_file_path(name=kwargs['name'])
        self._check_if_file_exists(filename=path)
        with open(path, 'r') as f:
            x = csv.reader(f, delimiter=',', quotechar='"')
            for row in x:
                data_list.append(row)
            return data_list

    def _get_file_path(self, *args, **kwargs):
        name = kwargs['name']
        root = os.path.abspath(os.path.join('..'))
        return f'{root}/data/{name}.csv'

    def _check_if_file_exists(self, *args, **kwargs):
        filename = kwargs['filename']
        if not os.path.isfile(filename):
            open(filename, 'a').close()
