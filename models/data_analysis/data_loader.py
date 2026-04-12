import pandas as pd

class DataLoader:
    def __init__(self, path):
        self.path = path

    def load(self):
        df = pd.read_csv(self.path, sep=';', header=8)
        return df