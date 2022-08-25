from controller.base_analytics import BaseAnalytics


class BaseStorageHandler:

    def upload_plot(self, img_data):
        raise NotImplementedError()

    def get_dataset(self):
        raise NotImplementedError()

    def upload_chunk(self, index):
        raise NotImplementedError()

    def get_model(self):
        raise NotImplementedError()

    def pre_upload_model(self, k, distance_function_type, date):
        raise NotImplementedError()

    def upload_model(self, k, distance_function_type):
        raise NotImplementedError()

    def update_analytics(self, analytics: BaseAnalytics, k: int, distance_function_type: int, date: int):
        raise NotImplementedError()

    def connect_mongo(self):
        raise NotImplementedError()

    @property
    def current_model_key(self):
        raise NotImplementedError()

