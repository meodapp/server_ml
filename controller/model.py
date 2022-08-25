import os
import pickle

from nltk.cluster import KMeansClusterer

from controller import MODEL_PATH, \
    DistanceFunctionEnum
from controller.base_model import BaseClusteringModel
from utils.exceptions import NoAvailableModelError


class ClusteringModel(BaseClusteringModel):

    def __init__(self, performed_procedures_cat=None, labels=None, *args, **kwargs):
        BaseClusteringModel.__init__(self, *args, **kwargs)
        self._labels = labels
        self.performed_procedures_cat = performed_procedures_cat


    def save(self, distance_function_type: int, date: int):
        self._save_raw(distance_function_type=distance_function_type, date=date)

    @property
    def labels(self):
        return self._labels

    @property
    def model(self) -> KMeansClusterer:
        if self._model:
            return self._model
        try:
            model = self.storage_handler.get_model()
            self._model = model
        except Exception:
            raise NoAvailableModelError()
        return self._model


    def _save_raw(self, distance_function_type: int, date: int):
        try:
            os.mkdir(MODEL_PATH)
        except FileExistsError:
            pass
        pickle.dump(self._model, open(f'{MODEL_PATH}/model.p', 'wb'))
        self.storage_handler.upload_model(k=self.model.num_clusters(), distance_function_type=distance_function_type,
                                          date=date)
