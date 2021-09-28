'''
Ryan Phillips

knapsack_genetic/standard/evolution.py
'''
from multiprocessing import Process
from .operations import (
  generate_init_population,
  breed_next_generation,
  l2norm
)

def evolve(data, args, testing):
  '''
  Simulates evolution until a generation is born that is not stupid
  '''
  data_idxs = range(len(data))
  population, sum_of_squares = generate_init_population(
    data, data_idxs,
    args.init_population,
    args.init_num_samples,
    args.max_weight)
  normal_fit = l2norm(population.fitnesses, sum_of_squares=sum_of_squares)

  tolerated, generations = 0, list()
  while tolerated < args.improvement_leniency:
    previous_avg_fitness = population.avg_fitness
    generations.append(population)

    population, sum_of_squares = breed_next_generation(
      data, data_idxs, population,
      args.max_weight, args.mutation_rate,
      normal_fitnesses=normal_fit,
      deallocate_ancestors=True)
    normal_fit = l2norm(population.fitnesses, sum_of_squares=sum_of_squares)

    if testing and len(generations) % 100 == 0:
      print('Generation: ', len(generations))
      print(population)

    improvement = population.avg_fitness - previous_avg_fitness
    if improvement < args.improvement_required:
      tolerated += 1 
    else:
      tolerated = 0

  return generations