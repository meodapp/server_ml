import pathlib

import pandas as pd
path = pathlib.Path(__file__).parent.parent.resolve()
class Terminology:
    def __init__(self):
        self.df = pd.read_csv(f"{path}/data/terminology.csv", sep=";", names=["category", "key", "value"], dtype={
                "key": "category"
            })
        self._series = {}
        self._performed_procedure = None

    @property
    def performed_procedure(self):
        if self._performed_procedure is not None:
            return self._performed_procedure
        self._performed_procedure = self.df[self.df['category'] == 'SUS']
        return self._performed_procedure

    def get_performed_procedure(self, key):
        performed_procedure = None
        try:
            performed_procedure = self.performed_procedure[self.performed_procedure['key'] == key].iloc[0]['value']
        except Exception:
            pass
        return performed_procedure

    def get_performed_procedures(self, keys):
        return [self.get_performed_procedure(str(key)) for key in keys]