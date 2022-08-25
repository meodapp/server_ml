import unittest

from controller.algorithm import Algorithm
from tests.storage_handler import TestStorageHandler, \
    TestStorageHandlerPopularTreatments, \
    TestStorageHandlerEqual
from utils.helpers import count_corrects


class TestClusteringEqual(unittest.TestCase):

    def test_clustering_equal(self):
        storage_handler = TestStorageHandlerEqual()
        algo = Algorithm(storage_handler=storage_handler, num_clusters=5)
        algo.create_model()
        corrects = 0
        corrects += count_corrects(algo.clustering_model.labels[0:5])
        corrects += count_corrects(algo.clustering_model.labels[5:10])
        corrects += count_corrects(algo.clustering_model.labels[10:15])
        corrects += count_corrects(algo.clustering_model.labels[15:20])
        corrects += count_corrects(algo.clustering_model.labels[20:25])
        print(f"labels: {algo.clustering_model.labels}")
        print(f"corrects: {corrects}")
        self.assertGreaterEqual(corrects / 25, 0.9)
