import unittest

from controller.algorithm import Algorithm
from tests.storage_handler import TestStorageHandler, \
    TestStorageHandlerPopularTreatments
from utils.helpers import count_corrects


class TestClustering(unittest.TestCase):

    def test_clustering(self):
        storage_handler = TestStorageHandler()
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
        self.assertGreaterEqual(corrects / 25, 0.72)


    def test_clustering_performed_procedures(self):
        storage_handler = TestStorageHandlerPopularTreatments()
        algo = Algorithm(storage_handler=storage_handler, num_clusters=10)
        algo.create_model()
        clusters = algo.clustering_model.labels
        df = algo.data.dataframe
        df['cluster'] = clusters
        correct = 0
        correct_60 = 0
        count = 0
        performed_procedures = df['performed_procedure'].value_counts()
        for performed_procedure in performed_procedures.index:
            performed_procedure_df = df[df['performed_procedure'] == performed_procedure]
            cluster_count = performed_procedure_df['cluster'].value_counts(normalize=True) * 100
            sorted_cluster_count = cluster_count.sort_values(ignore_index=True, ascending=False)
            # print(performed_procedure, sorted_cluster_count)
            correct += (sorted_cluster_count[0] >= 25)
            correct_60 += ((sum(sorted_cluster_count[:3])) >= 60)
            count += 1
        # print(f"correct: {correct}, correct_60: {correct_60}, count: {count}")
        self.assertGreaterEqual(correct / count, 0.80)
        self.assertGreaterEqual(correct_60 / count, 0.80)
