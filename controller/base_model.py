from nltk.cluster import VectorSpaceClusterer

from controller import DistanceFunctionEnum
from controller.storage_handler import BaseStorageHandler


class BaseClusteringModel:
    def __init__(self, storage_handler: BaseStorageHandler, model=None):
        self._model: VectorSpaceClusterer = model
        self.storage_handler = storage_handler

    def save(self, distance_function_type: int, date: int):
        raise NotImplementedError()

    def pre_save(self, distance_function_type: int, date: int):
        raise NotImplementedError()

    @property
    def model(self) -> VectorSpaceClusterer:
        raise NotImplementedError()

    @property
    def labels(self):
        raise NotImplementedError()