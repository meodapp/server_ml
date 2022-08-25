import numpy as np
import pandas as pd

from controller.storage_handler import BaseStorageHandler

class Cache:
    def __init__(self):
        self.value_count_of_field_min = dict()
        self.value_count_of_field_dict = dict()
        self.count_of_field_of_value_dict = dict()


class Data:
    def __init__(self, storage_handler: BaseStorageHandler = None, df=None, is_advanced_function=True):
        self.is_advanced_function = is_advanced_function
        self.filter_columns = None
        self._df = storage_handler.get_dataset() if df is None else df
        self.__set_fields()
        self.__cache = Cache()
        self.performed_procedure_cat = None
        self.gender_cat = None
        self.diagnosis_cat = None
        self._clean_df()



    def _clean_df(self):
        self._df.dropna(inplace=True)
        self._df.replace(r'^\s*$', 0, regex=True, inplace=True)
        self._df.replace('""', 0, inplace=True)
        # self._df.drop(columns=['hashed_patient_identifier'], inplace=True)
        self._df.drop(columns=['healthcare_unit', 'hashed_patient_identifier', 'issue_date'], inplace=True)
        self._df['is_discharged'] = (self._df['date_of_discharge'] != 0).astype(int)
        self._df['main_diagnosis_category'] = self._df['main_diagnosis'].map(lambda x: (ord(x[:1]) - 64))
        self._df['main_diagnosis_sub_category'] = self._df['main_diagnosis'].map(lambda x: (ord(x[1:2]) - 48))
        self.performed_procedure_cat = self._df['performed_procedure']
        self.gender_cat = self._df['gender']
        self.diagnosis_cat = self._df['main_diagnosis']
        # self._df[self.categorical] = self._df[self.categorical].replace(np.nan, 'NA')
        # self._df[self.numerical] = self._df[self.numerical].replace(np.nan, 0)
        self._set_categorical_type()
        if self.is_advanced_function:
            self._set_categorical_as_freq()
        else:
            self._set_categorical_as_byte()
        self._set_numerical_type()
        must_have_pos_values = ['weight', 'height']
        self._df[(self._df[must_have_pos_values] <= 0).any(axis=1)][must_have_pos_values] = self._df[(self._df[must_have_pos_values] > 2).all(axis=1)][must_have_pos_values].mean()
        self._df.drop(columns=['date_of_discharge'], inplace=True)

    def _set_categorical_type(self):
        self._df[self.categorical] = self._df[self.categorical].astype("category")

    def _set_numerical_type(self):
        self._df[self.numerical] = self._df[self.numerical].apply(pd.to_numeric)

    def _set_categorical_as_freq(self):
        for cat in self.categorical:
            self._df[cat] = self._df[cat].apply(lambda x: self.value_counts_dict(cat, x))
        self._df[self.categorical] = self._df[self.categorical].astype(float)

    def __set_fields(self):
        self._categorical = None
        self._numerical = None
        self.categorical = ['state', 'gender', 'race', 'nationality', 'reason_for_encounter',
                            'reason_for_discharge', 'associated_causes', 'main_diagnosis',
                            'secondary_diagnosis', 'ethnic_group',
                            'indicator_of_transplantation']
        self.numerical = ['age', 'weight', 'height',
                          'number_of_transplantation', 'performed_procedure', 'main_diagnosis_category',
                          'main_diagnosis_sub_category']
        # self.numerical += ['date_of_discharge']
        self.numerical += ['is_discharged']

    @property
    def dataframe(self):
        if not self.filter_columns:
            return self._df
        return self._df[self.filter_columns]

    @property
    def performed_procedures_cat(self):
        return self.performed_procedure_cat

    @property
    def genders_cat(self):
        return self.gender_cat

    @property
    def diagnosises_cat(self):
        return self.diagnosis_cat

    @property
    def categorical(self):
        return self._categorical

    @categorical.setter
    def categorical(self, value):
        self._categorical = list(filter(lambda feature: feature in self.filter_columns,
                                        value)) if self.filter_columns else value

    @property
    def numerical(self):
        return self._numerical

    @numerical.setter
    def numerical(self, value):
        self._numerical = list(filter(lambda feature: feature in self.filter_columns,
                                      value)) if self.filter_columns else value

    def format_new_row(self, X):
        X.dropna(inplace=True)
        X.replace(r'^\s*$', 0, regex=True, inplace=True)
        X.replace('""', 0, inplace=True)
        X.drop(columns=['healthcare_unit', 'hashed_patient_identifier', 'issue_date'], inplace=True)
        X['is_discharged'] = (X['date_of_discharge'] != 0).astype(int)
        X['main_diagnosis_category'] = X['main_diagnosis'].map(lambda x: (ord(x[:1]) - 64))
        X['main_diagnosis_sub_category'] = X['main_diagnosis'].map(lambda x: int(x[1:2]))
        X.drop(columns=['date_of_discharge'], inplace=True)
        # X[self.categorical] = X[self.categorical].replace(np.nan, 'NA')
        # X[self.numerical] = X[self.numerical].replace(np.nan, 0)
        X[self.categorical] = X[self.categorical].astype("category")
        if self.is_advanced_function:
            for cat in self.categorical:
                X[cat] = X[cat].apply(lambda x: self.value_counts_dict(cat, x))
        else:
            for cat in self.categorical:
                for cat in self.categorical:
                    X[cat] = X[cat].apply(lambda x: ("".join(format(x, 'b') for x in bytearray(str(x), 'utf-8'))))
        X[self.numerical] = X[self.numerical].apply(pd.to_numeric)
        return X

    # cache fn >
    def value_counts_min(self, field):
        try:
            return self.__cache.value_count_of_field_min[field]
        except Exception:
            self.__cache.value_count_of_field_min[field] = (self._df[field].value_counts(normalize=True) * 100).min()
        return self.__cache.value_count_of_field_min[field]

    def value_counts_dict(self, field: str, value: str):
        field_value_key = "{}{}".format(field, value)
        try:
            return self.__cache.count_of_field_of_value_dict[field_value_key]
        except Exception:
            try:
                value_count_of_field_dict = self.__cache.value_count_of_field_dict[field]
                count_of_field_of_value = value_count_of_field_dict[value]
                self.__cache.count_of_field_of_value_dict[field_value_key] = count_of_field_of_value
                return count_of_field_of_value
            except Exception:
                self.__cache.value_count_of_field_dict[field] = (
                        self._df[field].value_counts(normalize=True) * 100).to_dict()
                value_count_of_field_dict = self.__cache.value_count_of_field_dict[field]
                count_of_field_of_value = value_count_of_field_dict.get(value, 0)
                self.__cache.count_of_field_of_value_dict[field_value_key] = count_of_field_of_value
        return self.__cache.count_of_field_of_value_dict[field_value_key]

    # cache fn <
    def _set_categorical_as_byte(self):
        for cat in self.categorical:
            self._df[cat] = self._df[cat].apply(lambda x: ("".join(format(x, 'b') for x in bytearray(str(x), 'utf-8'))))
        self._df[self.categorical] = self._df[self.categorical].astype(float)

