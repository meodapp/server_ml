from io import StringIO

import pandas as pd
import pygad as pygad

from controller.algorithm import Algorithm
from tests.storage_handler import TestStorageHandler
from utils.helpers import most_com, \
    count_corrects


def get_score(labels):
    score = 0
    score += count_corrects(labels[0:5])
    first_batch_most_com = most_com(labels[0:5])
    score += count_corrects(labels[5:10])
    second_batch_most_com = most_com(labels[5:10])
    score += count_corrects(labels[10:15])
    third_batch_most_com = most_com(labels[10:15])
    score += count_corrects(labels[15:20])
    fourth_batch_most_com = most_com(labels[15:20])
    score += count_corrects(labels[20:25])
    fifth_batch_most_com = most_com(labels[20:25])
    arr = [first_batch_most_com , second_batch_most_com, third_batch_most_com, fourth_batch_most_com, fifth_batch_most_com]

    all_diff = 0
    for i in range(0, len(arr) - 1):
        if arr[i] == arr[i+1]:
            all_diff += 1
    if all_diff > 0:
        score -= all_diff*5
    else:
        score += 7
    return score

def init():
    initial_population = [[3, 10, 0.01, 0.05], [1, 5, 0.11, 0.15], [2, 8, 0.01, 0.15], [10, 10, 0.01, 0.5],
                       [10, 1, 1, 0.001],
                       [4, 2, 0.03, 0.03], [1, 1, 0.3, 0.001], [2, 2, 0.09, 0.02], [5, 3, 1, 0.01]]

    num_generations = 20
    num_parents_mating = 2

    num_genes = 4

    init_range_low = 0.01
    init_range_high = 100

    parent_selection_type = "sss"  # check this param
    keep_parents = 1  # check this param

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           initial_population=initial_population,
                           mutation_percent_genes=mutation_percent_genes)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    with open("hyperparams.csv", "a") as f:
        f.write(f"{','.join([str(abs(x)) for x in solution.tolist()])},{solution_fitness}\n")

def fitness_function(solution, solution_idx):
    storage_handler = TestStorageHandler()
    theta_1 = abs(solution[0])
    theta_2 = abs(solution[1])
    alpha = abs(solution[2])
    beta = abs(solution[3])
    algo = Algorithm(storage_handler=storage_handler, num_clusters=5, theta_1=theta_1, theta_2=theta_2, alpha=alpha, beta=beta)
    algo.create_model()
    labels = algo.clustering_model.labels

    score = get_score(labels)

    if score > 18:
        print(f"got score {score} with input {solution} // labels: {[labels[0:5], labels[5:10], labels[10:15], labels[15:20], labels[20:25]]}")
    return score





if __name__ == "__main__":
    init()
