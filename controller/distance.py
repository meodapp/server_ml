import math
import pathlib
from typing import Union, \
    List

import pandas as pd
from numpy import ndarray
from pandas import Series

from controller.base_distance import BaseDistanceFunction
from controller.data import Data
from controller.validations import Validations

MIXED_TYPE = Union[int, str]

path = pathlib.Path(__file__).parent.parent.resolve()
class Cache:
    def __init__(self, data: Data):
        self.data = data
        
        self.__field_index_no = dict()
        self.__a_k = dict()
        self.__cached_distance_of_two_values_of_attribute_ak_in_data_set = dict()

    def get_field_index(self, field):
        try:
            return self.__field_index_no[field]
        except Exception:
            self.__field_index_no[field] = self.data.dataframe.columns.get_loc(field)
        return self.__field_index_no[field]

    def get_a_k(self, field):
        try:
            return self.__a_k[field]
        except Exception:
            self.__a_k[field] = self.data.dataframe[field]
        return self.__a_k[field]

    def get_cached_distance_of_two_values_of_attribute_ak_in_data_set(self, a_k, v_i, v_j):
        try:
            key = "{}{}{}".format(a_k.name, v_i, v_j)
            return self.__cached_distance_of_two_values_of_attribute_ak_in_data_set[key]
        except Exception:
            try:
                key = "{}{}{}".format(a_k.name, v_j, v_i)
                return self.__cached_distance_of_two_values_of_attribute_ak_in_data_set[key]
            except Exception:
                pass

    def set_cached_distance_of_two_values_of_attribute_ak_in_data_set(self, key: str, distance: float):
        self.__cached_distance_of_two_values_of_attribute_ak_in_data_set[key] = distance


class DistanceFunction(BaseDistanceFunction):
    def __init__(self, data: Data, theta_1=None, theta_2=None, alpha=None, beta=None):
        self.data = data
        self.alpha, self.beta, self.theta_1, self.theta_2 = alpha, beta, theta_1, theta_2
        if theta_1 is None or theta_2 is None or alpha is None or beta is None:
            self.alpha, self.beta, self.theta_1, self.theta_2 = self._get_best_hyperparams()
        self._cache = Cache(data=data)

    def _get_best_hyperparams(self):
        df = pd.read_csv(f"{path}/utils/hyperparams.csv", dtype=float)
        df.sort_values(by="score", ascending=False, inplace=True)
        best = df.iloc[0]
        theta_1 = best['theta_1']
        theta_2 = best['theta_2']
        alpha = best['alpha']
        beta = best['beta']
        print(f"Using saved hyper-params theta_1={theta_1}, theta_2={theta_2}, alpha={alpha}, beta={beta}")

        return alpha, beta, theta_1, theta_2

    ## Eq 3 >
    def _f(self, z) -> float:
        return self.f(z, theta_1=self.theta_1, theta_2=self.theta_2, alpha=self.alpha, beta=self.beta)

    @staticmethod
    def f(z, theta_1=3, theta_2=10, alpha=0.01, beta=0.05) -> float:
        if z <= theta_1:
            return 1
        elif theta_1 < z <= theta_2:
            return round(1 - beta * (z - theta_1), 2)
        else:
            return round(1 - beta * (theta_2 - theta_1) - alpha * (z - theta_2), 2)

    def occurrence_frequency_of_a_value_of_ak(self, a_k: Series, v: MIXED_TYPE) -> int:
        #     calculates the occurrence frequency of a value
        if a_k.name in self.data.categorical:
            return v
        return self.data.value_counts_dict(a_k.name, v)

    def minimum_occurrence_frequency_of_all_values_of_attribute_ak(self, a_k: Series) -> float:
        # m f ak is the minimum occurrence frequency of all values of attribute ak
        return self.data.value_counts_min(a_k.name)


    def distance_of_two_values_of_attribute_ak(self, a_k: Series, v_i: MIXED_TYPE, v_j: MIXED_TYPE) -> float:
        #   To calculate the distance of two values of attribute ak
        frak_vi, frak_vj = self.frak(a_k, v_i), self.frak(a_k, v_j)
        Validations.no_list_full_of_zeros([frak_vi, frak_vj], **{"first": v_i, "second": v_j})
        numerator = abs(frak_vi - frak_vj) + self.mfak(a_k)
        denominator = max(frak_vi, frak_vj)
        return round(numerator / denominator, 2)

    ## Eq 3 <

    ## Eq 10 >
    def distance_of_two_values_of_attribute_ak_in_data_set(self, a_k: Series, v_i: MIXED_TYPE,
                                                           v_j: MIXED_TYPE) -> float:
        cache = self.get_cache()
        cached_distance = cache.get_cached_distance_of_two_values_of_attribute_ak_in_data_set(a_k=a_k, v_i=v_i, v_j=v_j)
        if cached_distance:
            return cached_distance
        distance = max(self.f(len(a_k)), self.dfrak(a_k, v_i, v_j), self.theta_1)
        cache.set_cached_distance_of_two_values_of_attribute_ak_in_data_set(
            key="{}{}{}".format(a_k.name, v_i, v_j), distance=distance)
        cache.set_cached_distance_of_two_values_of_attribute_ak_in_data_set(
            key="{}{}{}".format(a_k.name, v_j, v_i), distance=distance)
        return distance
    ## Eq 10 <

    ## Eq 11 >
    def categorical_distance_of_two_instances(self, item1: ndarray, item2: ndarray) -> int:
        cache = self.get_cache()
        dist = 0
        for field in self.data.categorical:
            index_no = cache.get_field_index(field)
            a_k = cache.get_a_k(field)
            v_i = item1[index_no]
            v_j = item2[index_no]
            if self.delta(v_i, v_j):
                dist += pow(self.wak(a_k=a_k, v_i=v_i, v_j=v_j), 2)
        return dist
    ## Eq 11 <

    ## Eq 12 >
    @staticmethod
    def categorical_delta(categorical_value_1: str, categorical_value_2: str):
        return 0 if categorical_value_1 == categorical_value_2 else 1

    ## Eq 12 <

    ## Eq 13 >
    def numeric_distance_of_two_instances(self, item1: ndarray, item2: ndarray) -> int:
        cache = self.get_cache()
        dist = 0
        for field in self.data.numerical:
            index_no = cache.get_field_index(field)
            v_j = item2[index_no]
            v_i = item1[index_no]
            dist += pow(v_i - v_j, 2)
        return dist
    ## Eq 13 <

    ## Eq 14 >
    def mixed_distance_of_two_instances(self, I_i: ndarray, I_j: ndarray) -> float:
        dist = math.sqrt(self.dist_num(I_i, I_j) + self.dist_cat(I_i, I_j))
        return dist
    ## Eq 14 <


    # shorter_name
    frak = occurrence_frequency_of_a_value_of_ak
    mfak = minimum_occurrence_frequency_of_all_values_of_attribute_ak
    dfrak = distance_of_two_values_of_attribute_ak
    wak = distance_of_two_values_of_attribute_ak_in_data_set
    delta = categorical_delta
    # shorter_name
    dist_cat = categorical_distance_of_two_instances
    dist_num = numeric_distance_of_two_instances
    dist_mix = mixed_distance_of_two_instances


    def get_cache(self):
        return self._cache if hasattr(self, '_cache') else self.__cache
    # cache fn <
