from datetime import datetime
from enum import IntEnum
from pathlib import Path


def get_date():
    return int(datetime.now().strftime("%Y%m%d"))


MODEL_BUCKET_NAME = 'kmeans-model-data'
DATA_BUCKET_NAME = 'medical-records-data-enc'
MODEL_PATH = Path(f"output/model/{get_date()}").absolute()


class DistanceFunctionEnum(IntEnum):
    Standard = 0
    Advanced = 1

