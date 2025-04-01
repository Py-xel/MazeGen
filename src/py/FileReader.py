import pandas as pd


class FileReader:
    DELIMITER = ";"

    def __init__(self):
        pass

    def read_from_csv(self, path: str) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_csv(path, delimiter=self.DELIMITER)
        return df.dropna()
