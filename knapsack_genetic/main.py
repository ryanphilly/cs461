'''
Ryan Phillips

knapsack_genetic/main.py

Script that runs the genetic algorithm
'''
from argparse import ArgumentParser

from utils import (
  abs_path,
  read_data,
  write_logs,
  cs461weight_constraint_fitness_func)

from maximizer import GeneticMaximizer

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

def evolve(data, args):
  '''
  Runs GA until specified convergence
  '''
  fitness_func = cs461weight_constraint_fitness_func(data, 5e2)

  maximizer = GeneticMaximizer( # init population created
    data, fitness_func,
    args.init_population_size,
    int(len(data) * args.init_items_frac),
    args.mutation_rate)

  tolerated, generation_avgs = 0, list()
  while tolerated < args.improvement_leniency:
    previous_avg_fitness = maximizer.population['avg_fitness']
    generation_avgs.append(previous_avg_fitness)

    maximizer.step() # next population bred

    improvement = maximizer.population['avg_fitness'] - previous_avg_fitness

    if len(generation_avgs) % 100 == 0:
      print('-' * 50)
      print('Generation: ', len(generation_avgs))
      print('Avg fitness: ', maximizer.population['avg_fitness'])
      print('-' * 25)
      print('Overall Best Fitness: ', maximizer.best_selection['fitness'])
      print('Overall Best chromosome: ', maximizer.best_selection['chromosome'])
      print('-' * 50)

    if improvement < args.improvement_required:
      tolerated += 1 
    else:
      tolerated = 0

  return maximizer.best_selection

evolve(data, args)