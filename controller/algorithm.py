from controller import get_date, \
    DistanceFunctionEnum
from controller.analytics import Analytics
from controller.base_clustering_algorithm import BaseClusteringAlgorithm
from controller.base_distance import BaseDistanceFunction
from controller.base_model import BaseClusteringModel
from controller.clustering_algorithm import ClusteringAlgorithmKMeans
from controller.data import Data
from controller.distance import DistanceFunction
from controller.model import ClusteringModel
from controller.standard_distance import StandardDistanceFunction
from controller.storage_handler import BaseStorageHandler



class Algorithm:
    def __init__(self, storage_handler: BaseStorageHandler, num_clusters: int = 12,
                 distance_function: int = DistanceFunctionEnum.Advanced.value, **hyperparams):
        self.__storage_handler = storage_handler
        self.data = Data(storage_handler=self.__storage_handler, is_advanced_function=distance_function == DistanceFunctionEnum.Advanced.value)
        self.distance_function_type = distance_function
        self.distance_function: BaseDistanceFunction = self._get_distance_function(distance_function,
                                                                                   hyperparams)
        print(self.distance_function_type)
        print(self.distance_function)
        self.clustering_algorithm: BaseClusteringAlgorithm = ClusteringAlgorithmKMeans(data=self.data,
                                                                                       num_clusters=num_clusters,
                                                                                       storage_handler=self.__storage_handler,
                                                                                       distance_function=self.distance_function)
        self.clustering_model: BaseClusteringModel

    def _get_distance_function(self, distance_function, hyperparams):
        return DistanceFunction(data=self.data, **hyperparams) \
            if distance_function is DistanceFunctionEnum.Advanced.value else \
            StandardDistanceFunction(data=self.data)

    def create_model(self, is_upload=True):
        date = get_date()
        if is_upload:
            self.__storage_handler.pre_upload_model(k=self.clustering_algorithm.num_clusters,
                                                    distance_function_type=self.distance_function_type, date=date)

        self.clustering_model = self.clustering_algorithm.fit(data=self.data)

        if is_upload:
            self.clustering_model.save(distance_function_type=self.distance_function_type, date=date)
            analytics = Analytics(data=self.data, clusters=self.clustering_model.labels,
                                  cluster_names=self.clustering_model.model.cluster_names())
            self.__storage_handler.update_analytics(analytics=analytics, k=self.clustering_model.model.num_clusters(),
                                                    distance_function_type=self.distance_function_type, date=date)

    def predict(self, X):
        self.clustering_model = ClusteringModel(storage_handler=self.__storage_handler)
        X_vector = X.to_numpy().flatten()
        print(f"predicting vector: {X_vector}")
        for i, mean in enumerate(self.clustering_model.model.means()):
            d = self.clustering_model.model._distance(X_vector, mean)
            print(f"distance of {i}: {d}")
        return self.clustering_model.model.classify(X_vector)

