import random

from nltk.cluster.kmeans import KMeansClusterer

from controller.base_clustering_algorithm import BaseClusteringAlgorithm
from controller.base_model import BaseClusteringModel
from controller.model import ClusteringModel


class ClusteringAlgorithmKMeans(BaseClusteringAlgorithm):
    random_obj = random.Random(1234)

    def fit(self, data) -> BaseClusteringModel:
        print("entered fit")
        print(f"num clusters: {self.num_clusters}")
        kmeans = KMeansClusterer(self.num_clusters, distance=self.distance_function.dist_mix, avoid_empty_clusters=True,
                                 rng=self.random_obj, repeats=1)
        print("after kmeans")
        vectors = data.dataframe.to_numpy()
        clusters = kmeans.cluster(vectors, assign_clusters=True, trace=True)
        print("after clustering")
        return ClusteringModel(model=kmeans, storage_handler=self.storage_handler, labels=clusters, performed_procedures_cat=self.data.performed_procedures_cat)
