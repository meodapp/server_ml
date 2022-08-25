class BaseDistanceFunction:
    def mixed_distance_of_two_instances(self, I_i, I_j, **kwargs) -> float:
        raise NotImplementedError()

    def categorical_distance_of_two_instances(self, item1, item2) -> int:
        raise NotImplementedError()

    def numeric_distance_of_two_instances(self, item1, item2) -> int:
        raise NotImplementedError()

    # shorter_name
    dist_cat = categorical_distance_of_two_instances
    dist_num = numeric_distance_of_two_instances
    dist_mix = mixed_distance_of_two_instances
