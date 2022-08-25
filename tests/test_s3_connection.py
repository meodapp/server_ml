import unittest
from unittest import skip

from controller.algorithm import Algorithm
from controller.data import Data


@skip
class TestConnectionS3(unittest.TestCase):
    def test_download(self):
        data = Data()
        self.assertIsNotNone(data._df)

    @skip
    def test_upload(self):
        algo = Algorithm()


