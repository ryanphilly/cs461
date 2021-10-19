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
  weight_constraint_fitness_func)

from generator import Generator

parser = ArgumentParser()
'''
knapsack configuration:
'''
parser.add_argument('--max_weight', type=float, default=5e2)

'''
genetic algorithm configuration
'''
parser.add_argument('--init_population', type=int, default=1000)
parser.add_argument('--init_items_frac', type=float, default=1/20)
parser.add_argument('--mutation_rate', type=float, default=1e-4)
parser.add_argument('--improvement_required', type=float, default=1e-1)
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
  fitness_func = weight_constraint_fitness_func(data, args.max_weight)
  generator = Generator(
    data, fitness_func,
    args.init_population,
    int(len(data)*args.init_items_frac),
    args.mutation_rate)

  tolerated, generation_avgs = 0, list()
  while tolerated < args.improvement_leniency:
    previous_avg_fitness = generator.population['avg_fitness']
    generation_avgs.append(previous_avg_fitness)
    generator.step()
    improvement = generator.population['avg_fitness'] - previous_avg_fitness
    if len(generation_avgs) % 100 == 0:
      print(generator.best_selection['fitness'])
    if improvement < args.improvement_required:
      tolerated += 1 
    else:
      tolerated = 0

  return generator.best_selection
  

evolve(data, args)