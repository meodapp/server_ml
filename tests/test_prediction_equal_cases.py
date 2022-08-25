import unittest
from io import StringIO

import pandas as pd

from controller.algorithm import Algorithm
from tests.storage_handler import TestStorageHandlerEqual


class TestPredictEqual(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.storage_handler = TestStorageHandlerEqual()
        cls.algo = Algorithm(storage_handler=cls.storage_handler, num_clusters=5)
        cls.algo.create_model()

    def _assert_in_cluster(self, new_row_to_predict, expected_cluster):
        new_row_df = pd.read_csv(new_row_to_predict, sep=",")
        new_row_formatted = self.algo.data.format_new_row(new_row_df)
        cluster = self.algo.predict(X=new_row_formatted)
        self.assertEqual(cluster, expected_cluster)

    def test_prediction_equal_cluster_0_dataset(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
        15460041,SP,d6d9ac9ced4cea71,200902,0604270038,0a4d84042d1c22d16b76fd264bb3c56be97b6be96fd047957ddbfaddf7968731,80,F,99,010,06,21,0,0000,E782,0000,0,066,150,Y,02
        """)
        self._assert_in_cluster(new_row_to_predict, 0)

    def test_prediction_equal_cluster_1_dataset(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
        30304651,SP,cc9daefad9847341,201211,0604280084,0a4d84042d1c22d1389299840ce4036f5f7983af216dbaf236b978c6d3307151,01,M,99,099,06,21,0,0000,J450,0000,0,08,70,N,00
        """)
        self._assert_in_cluster(new_row_to_predict, 1)

    def test_prediction_equal_cluster_2_dataset(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
        33775051,RJ,63062c781b822a31,201104,0604130023,0a4d84042d1c22d1adf2d98dc8f4c1851e6727fa2177e1252ce2ea3c21d2fbf1,45,F,99,010,06,21,0,0000,G300,0000,0,060,156,N,00
        """)
        self._assert_in_cluster(new_row_to_predict, 2)

    def test_prediction_equal_cluster_3_dataset(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
        38415621,RJ,5ca778e140b6b781,200906,0604360010,0a4d84042d1c22d1a59f1de351ce784da8dedb3d9c716abfaf902b7b6ca1e0f1,50,F,99,010,06,21,0,0000,E780,0000,0,061,156,N,00
        """)
        self._assert_in_cluster(new_row_to_predict, 3)

    def test_prediction_equal_cluster_4_dataset(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
        52592381,RJ,f88db3696854f741,201005,0601350073,0a4d84042d1c22d11116196ecff43e37515d9c0d6a763fc1,25,F,99,010,01,16,20090801,0000,N180,N188,0,080,160,N,00
        """)
        self._assert_in_cluster(new_row_to_predict, 4)
