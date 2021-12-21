import pandas

from utils.logger import get_logger


class ExcelReader:
    def __init__(self, filepath: str, header: int = 0, index_col: int = None):
        self.filepath = filepath
        self.header = header
        self.index_col = index_col

    def read(self):
        logger = get_logger()

        try:
            df = pandas.read_excel(self.filepath, index_col=self.index_col, header=self.header)
            return df
        except Exception as e:
            logger.exception(e)
            return None


class ExcelWriter:
    def __init__(self, filepath: str, df: pandas.DataFrame):
        self.filepath = filepath
        self.df = df

    def write(self):
        logger = get_logger()

        try:
            self.df.to_excel(self.filepath, index=False)
        except Exception as e:
            logger.exception(e)
            return None
