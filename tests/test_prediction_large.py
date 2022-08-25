import unittest
from io import StringIO

import pandas as pd

from controller.algorithm import Algorithm
from tests.storage_handler import TestStorageHandler, \
    TestStorageHandlerLarge


class TestPredictLarge(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.storage_handler = TestStorageHandlerLarge()
        cls.algo = Algorithm(storage_handler=cls.storage_handler, num_clusters=12)
        cls.algo.create_model()

    def _assert_in_cluster(self, new_row_to_predict, expected_cluster):
        new_row_df = pd.read_csv(new_row_to_predict, sep=",")
        new_row_formatted = self.algo.data.format_new_row(new_row_df)
        cluster = self.algo.predict(X=new_row_formatted)
        self.assertEqual(cluster, expected_cluster)

    def test_prediction_0(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                7607536,SC,d6d9ac9ced4cea73,201203,0604010095,b97dcd26a652493bfbad71ce3aca3f31647803677d10c8bb,58,F,99,10,6,21,0,0,K518,0000,0,058,155,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_1(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                10938982,RJ,c0654f99056dbf54,201206,0604620039,0a4d84042d1c22d1a1b86364ed625416ff8e217c6a50129c89141117c49513ee,57,M,99,10,6,21,0,0,E892,0000,0,083,164,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 4)

    def test_prediction_2(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                288176,PR,aaf36e57ad39f9f4,200909,0601350120,066dc1f1bf291e96ac2b8f38635ba260ceae1bc0158f08689fd8d0c8fcf55e16,80,F,99,10,1,51,20090901,0,M811,E782,0,055,160,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 5)

    def test_prediction_3(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                38724284,PI,63062c781b822a39,200908,0601140036,0a4d84042d1c22d12fe7d2e51a31f99aa0617609c35d05d8f0cc8fe678e2dc2a,15,M,99,10,1,21,0,0,L701,0000,0,062,175,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)

    def test_prediction_4(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                46313357,SP,7d8afc1e94348d20,200911,0601310012,d6af91ef02590b873854823ad585f6e9a69c568237ce6bbd,48,M,1,10,1,21,0,0,E220,0000,0,100,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 8)

    def test_prediction_5(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                323836,BA,bc43cd25edd51774,201104,0604230087,0a4d84042d1c22d1d84720e347038dcbbfe4fe43a2b170db2d87d423e7c78576,34,F,99,10,6,21,0,0,F201,0000,0,0,0,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 1)

    def test_prediction_6(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                2838983,SP,67c29f49a092408d,201106,0604270054,0a4d84042d1c22d18dd910c9c82f25efce60cf33d1aa6bc7f16caad6e0e585e3,63,M,99,10,6,28,0,0,E781,0000,0,085,172,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 1)

    def test_prediction_7(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                32534243,RS,5411d5e74d9b45fe,201107,0604600020,0a4d84042d1c22d1992564e9e7f767562cfdbddbd1bf9a788f9c0e5aac5f8691,62,M,1,10,6,21,0,0,L400,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 7)

    def test_prediction_8(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                6258362,GO,b20d0b2bd5a64934,200812,0601070089,53c6b820e5bf6e20b6ff41b91587e7ff7a3ab52e862f0752,10,F,99,10,1,21,0,0,G408,0000,0,0,120,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)

    def test_prediction_9(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                44560546,DF,26568d29ce71f8d1,200904,0601300041,d6af91ef02590b870efd17e0fc2f85adddc383f9ebc30292c1267a9a8c2c741e,80,F,99,10,1,21,0,0,E220,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 11)

    def test_prediction_10(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                31227240,SP,f635fe45af99e8bc,200906,0601070070,0a4d84042d1c22d11258b6e4d41be163ca389e5f0e4b50d80cf8292c6ad80519,46,F,99,10,1,21,0,0,G402,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)

    def test_prediction_11(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                15390869,PI,63062c781b822a39,200906,0601310012,d6af91ef02590b87d44311a539e570c8535ba8dc023e2c09,45,F,99,10,1,21,0,0,E220,0000,0,062,001,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 8)

    def test_prediction_12(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                44867629,BA,64731b92beae5c74,201011,0604110022,0a4d84042d1c22d1ee1067f0987e83bede96c02c530bc543306503c7fb9e3971,38,F,3,10,6,21,0,0,D250,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_13(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                47719525,SP,0f24082013238cf7,200910,0601140010,0a4d84042d1c22d1239d23483a0cd57f15483d9c40c121f6eced35e5e576ec27,53,F,99,10,1,21,0,0,L400,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)

    def test_prediction_14(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                51664796,SP,21dae260cbf3ac2d,201205,0604010036,0a4d84042d1c22d13456cdbdb3b1d8190e6b530452e2d856516bec277113306e,36,F,99,10,6,21,0,0,K513,0000,0,060,160,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_15(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                47807785,MG,e6d00fc939d08c21,201204,0604100019,0a4d84042d1c22d1a5b7f36a6e9c22b69ae3c15bb3ef1d61e54f3bf9a770dd1d,31,M,99,10,6,21,0,0,E232,0000,0,0,170,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_16(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                8523177,MG,9e2aa33875bf7601,201202,0604500084,066dc1f1bf291e965772d96b04e67313ff586745df0688c1,24,M,99,10,6,21,0,0,G401,0000,0,0,165,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 3)

    def test_prediction_17(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                50696873,SC,d6d9ac9ced4cea73,200808,0601070038,0a4d84042d1c22d15ff649aebc29b8ea51359d10daa97a39835178e317b74ece,17,F,99,10,1,21,0,0,G408,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)

    def test_prediction_18(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                15218966,SP,0a06cd43040876ce,201001,0601040023,0a4d84042d1c22d1350a761a4262f92fdb33213e933ee3a898ebf848be96540a,57,F,99,10,1,28,0,0,D638,B182,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)

    def test_prediction_19(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                52903569,SP,36e498d8ebe49b29,200907,0601350138,ee246c29c68dc0d9820e7021c738c56b56f0b9f87d7e4786,72,F,99,10,1,21,0,0,M805,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 5)

    def test_prediction_20(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                40973194,SC,d6d9ac9ced4cea73,201103,0604500084,8e5b129dd3e1af1888d9f63a31fd1b9e7d9e4b876fefaf76,56,M,99,10,6,21,0,0,G402,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 10)

    def test_prediction_21(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                47305205,SP,a5200554b57bbaa0,200910,0601310020,0a4d84042d1c22d16a2ba9288575def989bd6ff9a1844940bfb70992900f97d06031387adce7bdf4,53,F,99,10,1,21,0,0,E220,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 8)

    def test_prediction_22(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                8795679,PR,541d6b515b90c197,201204,0604500076,0a4d84042d1c22d18f8c4200c342f0e2e6676bb7700ee2f126837648365d62e4,42,M,99,10,6,21,0,0,G408,0000,0,100,159,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 3)

    def test_prediction_23(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                6505305,SP,36e498d8ebe49b29,201006,0604110022,0a4d84042d1c22d149de8d840d305ba30a43fa1cb20b1ab921f6d7bd5a067c17,43,F,99,10,6,21,0,0,D250,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_24(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                8751903,PR,a36d4f7f56e4734a,201204,0604340060,0a4d84042d1c22d1875ce23adc0c28fbc6150f5fec669061,55,M,99,10,6,21,0,0,Z944,0000,0,086,168,S,01
                """)
        self._assert_in_cluster(new_row_to_predict, 2)

    def test_prediction_25(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                873463,RJ,c0654f99056dbf54,201001,0601220021,066dc1f1bf291e96a75b8a2470c989f711dcd0ca8a5388bd,74,F,99,10,1,21,0,0,G308,G308,0,0,0,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 0)

    def test_prediction_26(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                50218209,RJ,c0654f99056dbf54,201206,0604130023,0a4d84042d1c22d1704cf4135b5bebc7592fe89e1b08b5bc3d080271a7f8fa7e,80,F,99,10,6,21,0,0,G308,0000,0,062,164,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_27(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                48488421,PR,f6e851d26d18eddf,201201,0604130082,22f48f0e33d8ff9f6bca3ba030714a03e4553af4cc24f188,80,M,99,10,6,21,0,0,G308,0000,0,076,165,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_28(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                48486011,PR,fe4b67de1273833a,201201,0604600020,0a4d84042d1c22d1b35dd2fa50a4a862804c75d2a60a1160c3e9b31ba097c6f9,58,M,99,10,6,21,0,0,L400,0000,0,098,174,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 7)

    def test_prediction_29(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                40023253,SP,ff3a0effcc502d3f,201111,0604130023,0a4d84042d1c22d13c1235e44f56e97b73ce5d2762626dfdd6444c2ed489902c,80,F,1,10,6,21,0,0,G308,0000,0,060,162,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_30(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                52047523,SP,084d93a9d2ae3131,201007,0604010095,d6af91ef02590b87cbc294469b10db34b5dd97c6b54adf20a2851efb06e1c82e,40,F,1,10,6,21,0,0,M45,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 9)

    def test_prediction_31(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                15283909,MG,f60ba6e85408c7aa,201103,0604600011,0a4d84042d1c22d128262bccb739a0341229488b1c9bb4fca490d4b6b3cc94ef,41,F,99,10,6,21,0,0,L400,0000,0,0,0,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 7)

    def test_prediction_32(self):
        new_row_to_predict = StringIO("""id_,state,healthcare_unit,issue_date,performed_procedure,hashed_patient_identifier,age,gender,race,nationality,reason_for_encounter,reason_for_discharge,date_of_discharge,associated_causes,main_diagnosis,secondary_diagnosis,ethnic_group,weight,height,indicator_of_transplantation,number_of_transplantation
                3999280,PR,77d8fe967b4481fa,200908,0601040058,0a4d84042d1c22d14f81f4cea79139f163a1a7e99f60b63b,57,M,99,10,1,21,0,0,D638,0000,0,000,000,N,00
                """)
        self._assert_in_cluster(new_row_to_predict, 6)
