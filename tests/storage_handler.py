import pathlib
import pickle

import pandas as pd

from controller import get_date
from controller.base_analytics import BaseAnalytics
from controller.storage_handler import BaseStorageHandler

path = pathlib.Path(__file__).parent.parent.resolve()


class TestStorageHandler(BaseStorageHandler):
    def __init__(self):
        self.chunks = 0

    def upload_model(self, k):
        pass

    def update_analytics(self, analytics: BaseAnalytics, k: int):
        # d = analytics.get_clusters_analytics()
        pass

    def connect_mongo(self):
        pass

    @property
    def current_model_key(self):
        return "1"

    def upload_plot(self, img_data):
        pass

    def get_dataset(self):
        return pd.read_csv(
            f"{path}/tests/data/similar_clusters_test_file.csv",
            index_col=False, dtype={
                "performed_procedure": "category"
            })

    def upload_chunk(self, index):
        self.chunks = index + 1

    def get_model(self):
        return pickle.load(open(f'output/model/{get_date()}/model.p', 'rb'))


class TestStorageHandlerEqual(TestStorageHandler):
    def get_dataset(self):
        return pd.read_csv(f"{path}/tests/data/similar_clusters_test_file_equal.csv", index_col=False, dtype={
            "performed_procedure": "category"
        })


class TestStorageHandlerPopularTreatments(TestStorageHandler):
    def get_dataset(self):
        return pd.read_csv(f"{path}/tests/data/popular_performed_procedures.csv", index_col=False, dtype={
            "performed_procedure": "category"
        })


class TestStorageHandler1(TestStorageHandler):
    def get_dataset(self):
        return pd.read_csv(f"{path}/tests/data/test_1.csv", index_col=False, dtype={
            "performed_procedure": "category"
        })


class TestStorageHandler4(TestStorageHandler):
    def get_dataset(self):
        return pd.read_csv(f"{path}/tests/data/test_5.csv", index_col=False, dtype={
            "performed_procedure": "category"
        })


class TestStorageHandlerLarge(BaseStorageHandler):
    def __init__(self):
        self.chunks = 0

    def upload_model(self, k):
        pass

    def update_analytics(self, analytics: BaseAnalytics, k: int):
        # d = analytics.get_clusters_analytics()
        pass

    def connect_mongo(self):
        pass

    @property
    def current_model_key(self):
        return "1"

    def upload_plot(self, img_data):
        pass

    def get_dataset(self):
        return pd.read_csv(
            f"{path}/tests/data/similar_clusters_100_2.csv",
            index_col=False, dtype={
                "performed_procedure": "category"
            })

    def upload_chunk(self, index):
        self.chunks = index + 1

    def get_model(self):
        return pickle.load(open(f'output/model/{get_date()}/model.p', 'rb'))
