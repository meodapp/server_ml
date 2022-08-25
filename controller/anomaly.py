import math

import numpy as np
from numpy import ndarray

from controller.data import Data

THRESHOLD = 5


class AnomalyDetector():
    def __init__(self, data: Data, clusters: ndarray):
        self.data = data
        self._treatment_lengths = self.data.dataframe['performed_procedure'].value_counts().to_dict()
        self._amount_of_treatments = len(self.data.dataframe)
        self.clusters = clusters

    def popularity_of_treatment(self, treatment: int) -> float:
        amount_of_treatment = self._treatment_lengths.get(treatment, 0)
        return (amount_of_treatment * 100) / self._amount_of_treatments

    def popularity_of_treatment_in_cluster(self, treatment: int, cluster_idx: int) -> float:
        data_in_cluster = self.data.dataframe.iloc[np.where(self.clusters == cluster_idx)]
        treatments_in_cluster = data_in_cluster['performed_procedure'].value_counts().to_dict()
        treatments_length_in_cluster = len(data_in_cluster)
        treatment_length_in_cluster = treatments_in_cluster.get(treatment, 0)
        if not treatment_length_in_cluster:
            print(f"treatments_in_cluster: {treatments_in_cluster}")
            print(f"treatment: {treatment}")
        return (treatment_length_in_cluster * 100) / np.sum(treatments_length_in_cluster)

    def is_ok(self, treatment: int, cluster_idx: int) -> bool:
        popularity_of_treatment_in_cluster = self.popularity_of_treatment_in_cluster(treatment, cluster_idx)
        popularity_of_treatment = math.sqrt(
            self.popularity_of_treatment(treatment))
        # print(f"popularity_of_treatment_in_cluster: {popularity_of_treatment_in_cluster}")
        # print(f"popularity_of_treatment: {popularity_of_treatment}")
        return popularity_of_treatment_in_cluster > popularity_of_treatment
