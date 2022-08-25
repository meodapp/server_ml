import io
import logging
import pickle

import boto3
import pandas as pd
import pymongo

from controller import MODEL_BUCKET_NAME, \
    get_date, \
    DATA_BUCKET_NAME
from controller.base_analytics import BaseAnalytics
from controller.base_storage_handler import BaseStorageHandler
from controller.model import MODEL_PATH

PROFILE_NAME = "personal"
logger = logging.getLogger('storage_handler')


class StorageHandler(BaseStorageHandler):
    def __init__(self):
        super(StorageHandler).__init__()
        self.conn = None
        session = boto3.Session(profile_name=PROFILE_NAME)
        s3 = session.client('s3')
        self.s3 = s3

    @property
    def current_model_key(self) -> dict:
        conn = self.connect_mongo()
        metadata = conn["metadata"]
        item = metadata.find_one()
        print(item)
        return item['model_version']

    def connect_mongo(self):
        """ A util for making a connection to mongo """
        if self.conn is not None:
            return self.conn
        mongo_uri = 'mongodb+srv://root:wildcat1@cluster0.6rycq.mongodb.net/meod-db?retryWrites=true&w=majority'
        conn = pymongo.MongoClient(mongo_uri)
        self.conn = conn['meod-db']
        return self.conn

    def update_analytics(self, analytics: BaseAnalytics, k: int, distance_function_type: int, date: int):
        d = analytics.get_clusters_analytics()
        conn = self.connect_mongo()
        analytics = conn["analytics"]
        print("updating analytics")
        analytics.update_one(
            {
                "date": date,
                "k": k,
                "distance_function_type": distance_function_type
            }, {
                "$set": {
                    "clusters": d,
                    "date": date,
                    "k": k,
                    "distance_function_type": distance_function_type
                }
            }, upsert=True)

    def pre_upload_model(self, k, distance_function_type, date):
        conn = self.connect_mongo()
        metadata = conn["metadata"]
        metadata.update_one({}, {
            '$push': {
                'model_versions': {
                    "date": date,
                    "k": k,
                    "distance_function_type": distance_function_type,
                    "ready": False
                }
            }
        }, upsert=True)

    def upload_model(self, k, distance_function_type, date):
        session = boto3.Session(profile_name='personal')
        s3 = session.client('s3')
        s3.upload_file(f'{MODEL_PATH}/model.p', MODEL_BUCKET_NAME, f'model_{k}_{date}_{distance_function_type}.p')

        conn = self.connect_mongo()
        metadata = conn["metadata"]

        metadata.update_one({
            "model_versions": {
                "$elemMatch": {
                    "date": date,
                    "k": k,
                    "distance_function_type": distance_function_type,
                    "ready": False,
                }
            }
        },
        {
            "$set": {
                "model_versions.$.ready": True
            }
        },
        upsert=False)

    def get_model(self):
        session = boto3.Session(profile_name='personal')
        s3 = session.client('s3')
        current_model = self.current_model_key
        print(f"current_model: {current_model}")
        body_obj = s3.get_object(Bucket=MODEL_BUCKET_NAME,
                                 Key=f'model_{current_model["k"]}_{current_model["date"]}_{current_model["distance_function_type"]}.p')
        model = pickle.loads(io.BytesIO(body_obj['Body'].read()).read())
        return model

    def get_dataset(self):
        session = boto3.Session(profile_name=PROFILE_NAME)
        s3 = session.client('s3')
        objects = s3.list_objects_v2(Bucket=DATA_BUCKET_NAME)
        prefix_df = []
        logger.info(msg="Appending datasets")
        for obj in objects.get('Contents'):
            file_name = obj.get('Key')
            body_obj = s3.get_object(Bucket=DATA_BUCKET_NAME, Key=file_name)
            df = pd.read_csv(io.BytesIO(body_obj['Body'].read()), index_col=False, dtype={
                "performed_procedure": "category"
            })
            prefix_df.append(df)
            logger.info(msg=f"dataset: {file_name}, length: {len(df)}")
        concat_df = pd.concat(prefix_df)
        logger.info(msg=f"Final dataset length: {len(concat_df)}")
        return concat_df

    def upload_plot(self, img_data):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(MODEL_BUCKET_NAME)
        bucket.put_object(Body=img_data, ContentType='image/png', Key=f"{get_date()}/Centers.png")
