'''
Ryan Phillips

knapsack_genetic/standard/evolution.py
'''

from multiprocessing import Process

from .operations import (
  generate_init_population,
  sp_crossover,
  evaluate_selection,
  l2norm
)

def evolve(data, args, testing):
  '''
  Simulates evolution until a generation is born that is not stupid
  '''
  data_idxs = range(len(data))
  population, fitnesses, avg_fitness, sum_of_squares = generate_init_population(
    data, data_idxs, args.init_population, args.init_num_samples, args.max_weight)
  avg_fitnesses = [ avg_fitness, ]

  def next_generation(population, normal_fit_sorted):
    pop_size = len(population)
    # drop least fit individual if needed
    if pop_size % 2 != 0: population.remove(normal_fit_sorted[0][0])
    new_population, new_fitnesses = list(), list()
    sum_of_squares, total_fitness = 0, 0
    population = [population[normal_fit_sorted[998][0]], population[normal_fit_sorted[999][0]]]*500
    for idx in range(pop_size // 2):
      son, daughter = sp_crossover(
        data_idxs,
        population[normal_fit_sorted[idx][0]],
        population[normal_fit_sorted[pop_size-idx-1][0]],
        args.mutation_rate)
      new_population.extend([son, daughter])
      son_fitness = evaluate_selection(data, son, args.max_weight)
      daughter_fitness = evaluate_selection(data, daughter, args.max_weight)
      new_fitnesses.extend([(idx*2, son_fitness), (idx*2+1, daughter_fitness)])
      sum_of_squares += son_fitness**2 + daughter_fitness**2
      total_fitness += son_fitness + daughter_fitness
  
    return new_population, new_fitnesses, total_fitness / pop_size, sum_of_squares

  previous_avg_fitness, num_terminations_hit = 0, 0
  improvement = avg_fitness - previous_avg_fitness
  while num_terminations_hit < args.terminates_needed:
    previous_avg_fitness = avg_fitness
    normal_fitnesses = l2norm(fitnesses, sum_of_squares=sum_of_squares)
    normal_fitnesses.sort(key=lambda x: x[1])
    population, fitnesses, avg_fitness, sum_of_squares = next_generation(
      population, normal_fitnesses)
    if testing:
      if len(avg_fitnesses) % 1000 == 0:
        print(avg_fitness)
    avg_fitnesses.append(avg_fitness)
    improvement = avg_fitness - previous_avg_fitness
    if improvement < args.terminate_improvement:
      num_terminations_hit += 1
    else:
      num_terminations_hit = 0

  return avg_fitnesses