import numpy as np
import pandas as pd
import pygad as pygad

from controller.algorithm import Algorithm
from controller.distance import DistanceFunction
from tests.storage_handler import TestStorageHandlerLarge
from tests.test_clustering import count_corrects
from utils.helpers import most_com


def get_score(labels, n, cluster_relations=[]):
    score = 0
    most_common_list = []

    for i in range(0, len(labels), n):
        score += count_corrects(labels[i:i + n])
        most_common_list.append(most_com(labels[i:i + n]))

    for cluster_relation in cluster_relations:
        if most_common_list[cluster_relation[0]] == most_common_list[cluster_relation[1]]:
            score += 3

    values_counts_diff_from_mean = _get_diff_from_mean_distribution(labels)

    score -= values_counts_diff_from_mean
    return score


def _get_diff_from_mean_distribution(labels):
    df = pd.DataFrame(labels, columns=['labels'])
    values_counts = (df['labels'].value_counts(normalize=True) * 100)
    values_counts_mean = values_counts.mean()
    values_counts_diff_from_mean = abs(values_counts - values_counts_mean).sum()
    return values_counts_diff_from_mean


def init():

    num_generations = 50
    num_parents_mating = 2

    num_genes = 4
    sol_per_pop = 4

    random_mutation_min_val = 0
    gene_type = [int, int, float, float]
    gene_space = [{'low': 1, 'high': 1000}, {'low': 1, 'high': 1000}, {'low': 0, 'high': 1}, {'low': 0, 'high': 1}]
    parent_selection_type = "rws"  # roulette
    keep_parents = 1  # How many parents we keep in the next generation

    crossover_type = "uniform"

    mutation_type = "random"
    mutation_probability = 0.1

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           num_genes=num_genes,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           gene_type=gene_type,
                           gene_space=gene_space,
                           sol_per_pop=sol_per_pop,
                           random_mutation_min_val=random_mutation_min_val,
                           mutation_probability=mutation_probability)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    with open("hyperparams.csv", "a") as f:
        f.write(f"{','.join([str(abs(x)) for x in solution.tolist()])},{solution_fitness}\n")


def fitness_function(solution, solution_idx):
    storage_handler_large = TestStorageHandlerLarge()
    theta_1, theta_2, alpha, beta,  = solution[0], solution[1], solution[2], solution[3]

    if not is_valid_distance_function_domain(alpha, beta, theta_1, theta_2):
        return 0.1

    algo_large = Algorithm(storage_handler=storage_handler_large, num_clusters=8, theta_1=theta_1, theta_2=theta_2,
                           alpha=alpha, beta=beta)
    algo_large.create_model()
    labels_large = algo_large.clustering_model.labels
    score = get_score(labels_large, n=3, cluster_relations=[
        (0, 14), (1, 2), (2, 6), (4, 11), (5, 10), (6, 22), (7, 13), (8, 15), (9, 19), (10, 12), (12, 17), (13, 18),
        (15, 16), (17, 23), (18, 20), (19, 25), (20, 21), (21, 32), (22, 24), (23, 30), (24, 26), (26, 27), (27, 28),
        (28, 29), (30, 31)
    ])

    if score > 100:
        print(
            f"got score {score} with input {solution} // labels: {np.array_split(labels_large, 33)}")
    return score


def is_valid_distance_function_domain(alpha, beta, theta_1, theta_2):
    if theta_1 >= theta_2:
        return False
    z_list = [1, 10, 50, 75]
    for z in z_list:
        res = DistanceFunction.f(z, theta_1=theta_1, theta_2=theta_2, alpha=alpha, beta=beta)
        if not (0 <= res <= 1):
            return False
    return True


if __name__ == "__main__":
    init()
