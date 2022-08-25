from utils.exceptions import ParametersError

class Validations:
    @staticmethod
    def no_list_full_of_zeros(lst, **kwargs):
        if lst and (all(x == 0 for x in lst)):
            raise ParametersError("Every value in list is equal to zero for parameters: {params}".format(params=kwargs))


