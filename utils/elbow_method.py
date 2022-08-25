from matplotlib import pyplot as plt

from controller import DistanceFunctionEnum
from controller.algorithm import Algorithm
from controller.storage_handler import StorageHandler


class Elbow:

    @staticmethod
    def _get_inertia(clustering_model, data):
        inertia = 0
        vectors = data.dataframe.to_numpy()
        clusters = clustering_model.model.cluster(vectors, True)
        means = clustering_model.model.means()
        for i, x in enumerate(vectors):
            d = clustering_model.model._distance(x, means[clusters[i]])
            inertia += d ** 2
        return inertia

    def elbow_check(self, k_clusters=range(2, 50, 2), is_upload=True):
        storage_handler = StorageHandler()
        distortions = []
        for i, k in enumerate(k_clusters):
            algo = Algorithm(storage_handler=storage_handler, num_clusters=k, distance_function=DistanceFunctionEnum.Standard.value)
            algo.create_model(is_upload=False)
            distortions.append(self._get_inertia(clustering_model=algo.clustering_model, data=algo.data))
            print(distortions)
            try:
                self._plot_elbow_check(distortion_list=distortions)
            except Exception as err:
                print(err)

    @staticmethod
    def _plot_elbow_check(distortion_list):
        plt.figure(figsize=(16, 8))
        plt.plot(range(1, len(distortion_list) + 1), distortion_list, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal k')
        plt.show()

    @staticmethod
    def _analyze_elbow_check(distortion_list):
        print(sorted(enumerate(distortion_list), key=lambda d: d[1], reverse=True))


if __name__ == "__main__":
    # elbow_check()
    e = Elbow()
    distortion_list = [189993653309185.23,
189993653309185.23,
89993653309185.23,
89993653309185.23,
65654951204554.586,
65654951204554.586,
50654951204554.586,
50654951204554.586,
19358580759328.727,
19358580759328.727,
8166772874733.155,
8166772874733.155,
3036193403355.686,
3036193403355.686,
5071820618799.635,
5071820618799.635,
2403387581140.5645,
2403387581140.5645,
1816133549018.268,
1816133549018.268,
1250449531095.516,
1250449531095.516,
1687297354936.0022,
1687297354936.0022,
1131539563142.4036,
1131539563142.4036,
1115094326666.6667,
1115094326666.6667,
1130697537892.6104,
1130697537892.6104,
746825731267.3921,
746825731267.3921,
733962425016.0054,
733962425016.0054,
694726317305.8053,
694726317305.8053,
494665285401.5278,
494665285401.5278,
517262645120.9261,
517262645120.9261,
605114519505.2946,
605114519505.2946,
358382018762.2489,
358382018762.2489,
395613367596.7567,
395613367596.7567]
    distortion_list = [(x - abs(x - distortion_list[i+1])/2) if x == distortion_list[i-1] else x for i, x in enumerate(distortion_list[:-1])]
    e._plot_elbow_check(distortion_list=distortion_list)
    # e._analyze_elbow_check(distortion_list=distortion_list)
