'''
Ryan Phillips

knapsack_genetic/main.py

Script that runs the genetic algorithm
'''
from argparse import ArgumentParser

from utils import (
  abs_path,
  read_data,
  logger,
  cs461weight_constraint_fitness_func)

from maximizer import GeneticMaximizer


def evolve(data, args, verbose=True):
  '''
  Runs GA until specified convergence
  '''
  write_avg, write_100, save_pop, close_all_logs = logger(args.log_path)
  fitness_func = cs461weight_constraint_fitness_func(data, 5e2)

  maximizer = GeneticMaximizer( # init population created
    data, fitness_func,
    args.init_population_size,
    int(len(data) * args.init_items_frac),
    args.mutation_rate)

  tolerated, num_gens = 0, 1
  while tolerated < args.improvement_leniency:
    previous_avg_fitness = maximizer.population['avg_fitness']
    write_avg(previous_avg_fitness)

    maximizer.step() # next population bred
    num_gens += 1

    if num_gens % 10 == 0:
      save_pop(maximizer.population['chromosomes'])
    
    if num_gens % 100 == 0:
      write_100(maximizer, num_gens)
      if verbose:
        print('-' * 50)
        print('Generation: ', num_gens)
        print('Current Population Avg fitness: ', maximizer.population['avg_fitness'])
        print('Overall Best Fitness: ', maximizer.best_selection['fitness'])
        print('Overall Best chromosome: ', maximizer.best_selection['chromosome'])
        print('-' * 50, '\n')
    
    improvement = ((maximizer.population['avg_fitness'] - previous_avg_fitness) / previous_avg_fitness)
    if improvement * 100 < args.improvement_required:
      tolerated += 1
    else:
      tolerated = 0

  close_all_logs()
  return maximizer.best_selection, maximizer.population


if __name__ == '__main__':
  parser = ArgumentParser()
  '''
  genetic algorithm configuration
  '''
  parser.add_argument('--init_population_size', type=int, default=1000)
  parser.add_argument('--init_items_frac', type=float, default=1/20)
  parser.add_argument('--mutation_rate', type=float, default=1e-4)

  '''
  convergence specifications
  '''
  parser.add_argument('--improvement_required', type=float, default=1e-2)
  parser.add_argument('--improvement_leniency', type=int, default=10)

  '''
  input and log path configuration
  '''
  parser.add_argument('--data_path', type=str, default=abs_path('./data/'))
  parser.add_argument('--log_path', type=str, default=abs_path('./logs/'))

  args = parser.parse_args()
  data = read_data(args.data_path)
  print('Number of items in knapsack: ', len(data))

  print('Running genetic optimizer......')
  print('To stop before convergence with logs press ctrl c...')
  
  best, full_pop = evolve(data, args, verbose=True)

