import os
import pandas


class ExcelReader:
    def __init__(self, filepath: str, header: int = 0, index_col: int = None):
        self.filepath = filepath
        self.header = header
        self.index_col = index_col

    def read(self):
        try:
            df = pandas.read_excel(self.filepath, index_col=self.index_col, header=self.header)
            return df
        except Exception as e:
            print(e)
            return None
