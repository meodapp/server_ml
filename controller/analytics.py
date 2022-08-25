from numpy import ndarray

from controller.base_analytics import BaseAnalytics
from controller.data import Data
from controller.terminology import Terminology
from data.grupos import groups

THRESHOLD = 5


class Analytics(BaseAnalytics):
    def __init__(self, data: Data, clusters: ndarray, cluster_names):
        self.data = data
        self._treatment_lengths = self.data.performed_procedure_cat.value_counts().to_dict()
        self._amount_of_treatments = len(self.data.dataframe)
        self.clusters = clusters
        self.cluster_names = cluster_names

    def get_clusters_analytics(self):
        analytics_by_cluster = dict()
        cluster_indexes = dict()
        terminology = Terminology()
        print("get_clusters_analytics")
        for cluster_idx in self.cluster_names:
            print(f"creating analytic for cluster_id: {cluster_idx}")
            cluster_indexes[cluster_idx] = [(True if x == cluster_idx else False) for x in self.clusters]

            treatments_in_cluster = self.data.performed_procedure_cat.iloc[cluster_indexes[cluster_idx]]
            treatments_in_cluster_value_counts = (treatments_in_cluster.value_counts(normalize=True) * 100).to_dict()


            analytics_by_cluster[cluster_idx] = {str(key): {
                "probability": value,
                "group": self._get_treatment_group(treatment=str(key)),
                "display_name": terminology.get_performed_procedure(str(key)),
                "age_distribution": self._get_age_distribution(treatment=key, treatments_in_cluster=treatments_in_cluster),
                "gender_distribution": self._get_gender_distribution(treatment=key, treatments_in_cluster=treatments_in_cluster),
                "diagnosis_distribution": self._get_diagnosis_distribution(treatment=key, treatments_in_cluster=treatments_in_cluster)
            } for key, value in treatments_in_cluster_value_counts.items() if value > 0}
            print(f"{len(analytics_by_cluster[cluster_idx])} amount of treatments for cluster {cluster_idx}")
        print("finished creating analytics")
        return [analytics_by_cluster[key] for key in sorted(analytics_by_cluster)]

    def _get_gender_distribution(self, treatment, treatments_in_cluster):
        treatment_indexes_in_cluster = treatments_in_cluster[treatments_in_cluster == treatment].index
        gender_in_treatment_in_cluster = self.data.genders_cat.iloc[treatment_indexes_in_cluster]
        gender_in_treatment_in_cluster_value_counts = (
                gender_in_treatment_in_cluster.value_counts(normalize=True) * 100).to_dict()
        return gender_in_treatment_in_cluster_value_counts

    def _get_diagnosis_distribution(self, treatment, treatments_in_cluster):
        treatment_indexes_in_cluster = treatments_in_cluster[treatments_in_cluster == treatment].index
        diagnosis_in_treatment_in_cluster = self.data.diagnosis_cat.iloc[treatment_indexes_in_cluster]
        diagnosis_in_treatment_in_cluster_value_counts = (
                diagnosis_in_treatment_in_cluster.value_counts(normalize=True) * 100).to_dict()
        return diagnosis_in_treatment_in_cluster_value_counts

    def _get_age_distribution(self, treatment, treatments_in_cluster):
        treatment_indexes_in_cluster = treatments_in_cluster[treatments_in_cluster == treatment].index
        age_in_treatment_in_cluster = self.data.dataframe.age.iloc[treatment_indexes_in_cluster]
        age_in_treatment_in_cluster_value_counts = (
                age_in_treatment_in_cluster.value_counts(bins=[0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80], normalize=True) * 100).to_dict()
        age_in_treatment_in_cluster_value_counts_dict = {
            f"{int(key.left)}-{int(key.right)}": value for key, value in
            age_in_treatment_in_cluster_value_counts.items()
        }
        return age_in_treatment_in_cluster_value_counts_dict

    def _get_treatment_group(self, treatment):
        group = treatment[:2]
        sub_group = treatment[2:4]
        organization = treatment[4:6]
        try:
            group_obj = next(x for x in groups if x.get('co_grupo') == group)
            sub_group_obj = next(x for x in group_obj.get('sub_grupos') if x.get('co_sub_grupo') == sub_group)
            organization_obj = next(x for x in sub_group_obj.get('formas_organizacao') if x.get('co_forma_organizacao') == organization)
            return organization_obj.get('no_forma_organizacao')
        except Exception as err:
            print (err)
            return f"{group}{sub_group}{organization}"