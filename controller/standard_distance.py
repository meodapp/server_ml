from itertools import zip_longest

import numpy as np
from numpy import ndarray

from controller.base_distance import BaseDistanceFunction
from controller.data import Data
from controller.distance import Cache


def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip_longest(str(s1), str(s2)))

class StandardDistanceFunction(BaseDistanceFunction):

    def __init__(self, data: Data):
        self.data = data
        self._cache = Cache(data=data)

    def categorical_distance_of_two_instances(self, item1: ndarray, item2: ndarray) -> int:
        dist = 0
        for field in self.data.categorical:
            index_no = self._cache.get_field_index(field)
            v_i = item1[index_no]
            v_j = item2[index_no]
            dist += hamming_distance(str(v_i), str(v_j))
        return dist

    def numeric_distance_of_two_instances(self, item1: ndarray, item2: ndarray) -> int:
        dist = 0
        for field in self.data.numerical:
            index_no = self._cache.get_field_index(field)
            v_j = item2[index_no]
            v_i = item1[index_no]
            dist += np.linalg.norm(v_j - v_i)
        return dist

    def mixed_distance_of_two_instances(self, I_i: ndarray, I_j: ndarray) -> float:
        dist = self.dist_num(I_i, I_j) + self.dist_cat(I_i, I_j)
        return dist

    # shorter_name
    dist_cat = categorical_distance_of_two_instances
    dist_num = numeric_distance_of_two_instances
    dist_mix = mixed_distance_of_two_instances
