import time
import unittest
from unittest import skip

from controller.data import Data
from controller.distance import DistanceFunction
from tests.storage_handler import TestStorageHandler1
from utils.exceptions import ParametersError


class TestDistance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.startTime = time.time()
        storage_handler = TestStorageHandler1()
        cls.data = Data(storage_handler=storage_handler)
        cls.df = cls.data.dataframe
        cls.d = DistanceFunction(data=cls.data, theta_1=3, theta_2=10, alpha=0.01, beta=0.05)


## Eq 3 >
    def test_f_z_lower_than_thetha_1(self):
        self.assertEqual(DistanceFunction.f(1), 1)

    def test_f_z_equal_than_thetha_1(self):
        self.assertEqual(DistanceFunction.f(3, theta_1=3), 1)

    def test_f_z_between_thetha_1_and_theta_2(self):
        self.assertEqual(DistanceFunction.f(z=5, theta_1=3, theta_2=10), 0.9)

    def test_f_z_equal_than_theta_2(self):
        self.assertEqual(DistanceFunction.f(z=10, theta_1=3, theta_2=10), 0.65)

    def test_f_z_greater_than_thetha_2(self):
        self.assertEqual(DistanceFunction.f(z=100, theta_1=3, theta_2=10), -0.25)

    @skip("not relevant")
    def test_f_cache_time(self):
        for i in range(100000):
            DistanceFunction.f(z=100, theta_1=3, theta_2=10)
            DistanceFunction.f(z=10, theta_1=3, theta_2=10)
            DistanceFunction.f(z=5, theta_1=3, theta_2=10)
        print("With cache: {}".format(time.time() - self.startTime))
        self.assertLess(time.time() - self.startTime, 0.4)

    @skip("not relevant")
    def test_f_miss_cache_time(self):
        for i in range(100000):
            DistanceFunction.f(z=i, theta_1=3, theta_2=10)
            DistanceFunction.f(z=i, theta_1=3, theta_2=10)
            DistanceFunction.f(z=i, theta_1=3, theta_2=10)
        print("NO cache: {}".format(time.time() - self.startTime))
        self.assertLess(time.time() - self.startTime, 0.6)

    def test_occurrence_frequency_of_a_value_of_ak(self):
        self.assertEqual(self.d.occurrence_frequency_of_a_value_of_ak(self.df['age'], 63), 4/122*100)
        print(self.df)

    def test_no_occurrence_frequency_of_a_value_of_ak(self):
        self.assertEqual(self.d.occurrence_frequency_of_a_value_of_ak(self.df['age'], 1000), 0)

    def test_minimum_occurrence_frequency_of_all_values_of_attribute_ak(self):
        self.assertEqual(self.d.minimum_occurrence_frequency_of_all_values_of_attribute_ak(self.df['age']), 1/122*100)


    def test_distance_of_two_values_of_attribute_ak_numeric(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak(self.df['age'], 64, 72), 0.75)


    def test_distance_of_two_values_of_attribute_ak_categorical(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak(self.df['main_diagnosis'], self.data.value_counts_dict('main_diagnosis', 'N180'), self.data.value_counts_dict('main_diagnosis', 'M810')), 1.33)
        print(self.df)

    def test_no_distance_of_two_values_of_attribute_ak(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak(self.df['main_diagnosis'], self.data.value_counts_dict('main_diagnosis', 'N180'), self.data.value_counts_dict('main_diagnosis', 'N180')), 0.67)

    def test_only_one_distance_of_two_values_of_attribute_ak(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak(self.df['main_diagnosis'], self.data.value_counts_dict('main_diagnosis', 'N180'), self.data.value_counts_dict('main_diagnosis', 'lalalalwrongvalue')), 1.67)

    def test_wrong_parameters_distance_of_two_values_of_attribute_ak(self):
        with self.assertRaises(ParametersError) as context:
            self.d.distance_of_two_values_of_attribute_ak(self.df['main_diagnosis'],  self.data.value_counts_dict('main_diagnosis', 'lalalalwrongvalue'), self.data.value_counts_dict('main_diagnosis', 'lalalalwrongvalue2'))
        self.assertTrue("Every value in list is equal to zero for parameters: {'first': 0, 'second': 0}" in context.exception.args)

## Eq 3 <
## Eq 10 >
    def test_distance_of_two_values_of_attribute_ak_in_data_set_numeric(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak_in_data_set(self.df['age'], 64, 72), 3)

    def test_distance_of_two_values_of_attribute_ak_in_data_set_categorical(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak_in_data_set(self.df['main_diagnosis'], self.data.value_counts_dict('main_diagnosis', 'N180'), self.data.value_counts_dict('main_diagnosis', 'M810')), 3)

    def test_only_one_distance_of_two_values_of_attribute_ak_in_data_set(self):
        self.assertEqual(self.d.distance_of_two_values_of_attribute_ak_in_data_set(self.df['main_diagnosis'], self.data.value_counts_dict('main_diagnosis', 'N180'), self.data.value_counts_dict('main_diagnosis', 'lalalalwrongvalue')), 3)

    def test_wrong_parameters_distance_of_two_values_of_attribute_ak_in_data_set(self):
        with self.assertRaises(ParametersError) as context:
            self.d.distance_of_two_values_of_attribute_ak_in_data_set(self.df['main_diagnosis'], self.data.value_counts_dict('main_diagnosis', 'lalalalwrongvalue'), self.data.value_counts_dict('main_diagnosis', 'lalalalwrongvalue2'))
        self.assertTrue("Every value in list is equal to zero for parameters: {'first': 0, 'second': 0}" in context.exception.args)

## Eq 10 <

## Eq 11 >
    def test_categorical_distance_of_two_instances(self):
        item1 = self.df.iloc[0].to_numpy()
        item2 = self.df.iloc[1].to_numpy()
        dist = self.d.categorical_distance_of_two_instances(item1=item1, item2=item2)
        self.assertEqual(27, dist)

    def test_categorical_distance_of_two_instances_3(self):
        item1 = self.df.iloc[0].to_numpy()
        item2 = self.df.iloc[2].to_numpy()
        dist = self.d.categorical_distance_of_two_instances(item1=item1, item2=item2)
        self.assertEqual(36, dist)

    def test_categorical_distance_of_two_instances_2(self):
        item1 = self.df.iloc[13].to_numpy()
        item2 = self.df.iloc[8].to_numpy()
        self.assertEqual(45, self.d.categorical_distance_of_two_instances(item1=item1, item2=item2))

    def test_categorical_distance_of_two_instances_equal(self):
        item1 = self.df.iloc[119].to_numpy()
        item2 = self.df.iloc[120].to_numpy()
        self.assertEqual(0, self.d.categorical_distance_of_two_instances(item1=item1, item2=item2))

    def test_categorical_distance_of_two_instances_not_equal(self):
        item1 = self.df.iloc[120].to_numpy()
        item2 = self.df.iloc[121].to_numpy()
        self.assertEqual(99, self.d.categorical_distance_of_two_instances(item1=item1, item2=item2))
## Eq 11 <


## Eq 13 >
    def test_numerical_distance_of_two_instances(self):
        item1 = self.df.iloc[0].to_numpy()
        item2 = self.df.iloc[1].to_numpy()
        dist = self.d.numeric_distance_of_two_instances(item1=item1, item2=item2)
        self.assertEqual(9278, dist)

    def test_numerical_distance_of_two_instances_3(self):
        item1 = self.df.iloc[0].to_numpy()
        item2 = self.df.iloc[2].to_numpy()
        dist = self.d.numeric_distance_of_two_instances(item1=item1, item2=item2)
        self.assertEqual(4388, dist)

    def test_numerical_distance_of_two_instances_2(self):
        item1 = self.df.iloc[13].to_numpy()
        item2 = self.df.iloc[8].to_numpy()
        self.assertEqual(1156, self.d.numeric_distance_of_two_instances(item1=item1, item2=item2))

    def test_numerical_distance_of_two_instances_equal(self):
        item1 = self.df.iloc[119].to_numpy()
        item2 = self.df.iloc[120].to_numpy()
        self.assertEqual(0, self.d.numeric_distance_of_two_instances(item1=item1, item2=item2))

    def test_numerical_distance_of_two_instances_not_equal(self):
        item1 = self.df.iloc[120].to_numpy()
        item2 = self.df.iloc[121].to_numpy()
        self.assertEqual(30461.0, self.d.numeric_distance_of_two_instances(item1=item1, item2=item2))
## Eq 13 <

## Eq 14 >
    def test_mixed_distance_of_two_instances(self):
        item1 = self.df.iloc[0].to_numpy()
        item2 = self.df.iloc[1].to_numpy()
        dist = self.d.mixed_distance_of_two_instances(I_i=item1, I_j=item2)
        self.assertEqual(96.46242791885346, dist)

    def test_mixed_distance_of_two_instances_3(self):
        item1 = self.df.iloc[0].to_numpy()
        item2 = self.df.iloc[2].to_numpy()
        dist = self.d.mixed_distance_of_two_instances(I_i=item1, I_j=item2)
        self.assertEqual(66.51315659326356, dist)

    def test_mixed_distance_of_two_instances_2(self):
        item1 = self.df.iloc[13].to_numpy()
        item2 = self.df.iloc[8].to_numpy()
        self.assertEqual(34.655446902326915, self.d.mixed_distance_of_two_instances(I_i=item1, I_j=item2))

    def test_mixed_distance_of_two_instances_equal(self):
        item1 = self.df.iloc[119].to_numpy()
        item2 = self.df.iloc[120].to_numpy()
        self.assertEqual(0, self.d.mixed_distance_of_two_instances(I_i=item1, I_j=item2))

    def test_mixed_distance_of_two_instances_not_equal(self):
        item1 = self.df.iloc[120].to_numpy()
        item2 = self.df.iloc[121].to_numpy()
        self.assertEqual(174.81418706729727, self.d.mixed_distance_of_two_instances(I_i=item1, I_j=item2))
## Eq 14 <
