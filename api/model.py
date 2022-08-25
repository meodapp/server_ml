from typing import List, \
    Dict

import pandas as pd
from fastapi import APIRouter, \
    Query
from starlette import status

from api.interface import MedicalRecord, \
    Prediction
from controller.algorithm import Algorithm, \
    DistanceFunctionEnum
from controller.storage_handler import StorageHandler
from controller.terminology import Terminology
from tasks import update_all, \
    run_elbow_method

router = APIRouter()


@router.get("/update", status_code=status.HTTP_201_CREATED)
def _update(k: int, distance_function: int = Query(
                default=DistanceFunctionEnum.Advanced.value,
                title='Distance function',
            )):
    update_all.delay(k=k, distance_function=distance_function)
    return {
        "status": "CREATED"
    }

@router.post("/predict", status_code=status.HTTP_200_OK)
def predict(medical_record_dict: Dict) -> Prediction:
    print("Got request for predict")
    medical_record = MedicalRecord.parse_obj(medical_record_dict)
    print(medical_record)
    storage_handler = StorageHandler()
    print(storage_handler)
    algo = Algorithm(storage_handler=storage_handler)
    print(algo)
    X = algo.data.format_new_row(pd.json_normalize(medical_record.dict()))
    print(X)
    prediction = algo.predict(X)
    print(f"prediction: {prediction}")
    return Prediction(cluster=prediction)

@router.get("/get_performed_procedures", status_code=status.HTTP_200_OK)
def get_performed_procedures(codes: List[str] = Query(None)) -> List[str]:
    terminology = Terminology()
    return terminology.get_performed_procedures(codes)


@router.get("/elbow", status_code=status.HTTP_200_OK)
def _run_elbow_method():
    run_elbow_method.delay()
    return {
        "status": "RUNNING"
    }
