from pandas import DataFrame

from controller.base_distance import BaseDistanceFunction
from controller.base_model import BaseClusteringModel
from controller.storage_handler import BaseStorageHandler


class BaseClusteringAlgorithm:
    def __init__(self, data, num_clusters, storage_handler: BaseStorageHandler, distance_function: BaseDistanceFunction):
        self.data = data
        self.num_clusters = num_clusters
        self.storage_handler = storage_handler
        self.distance_function = distance_function

    def fit(self, data) -> BaseClusteringModel:
        raise NotImplementedError()
