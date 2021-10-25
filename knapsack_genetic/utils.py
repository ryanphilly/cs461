'''
Ryan Phillips
genetics/utils.py
'''
from os import path, mkdir
from glob import glob

def l2norm(fitnesses):
  '''
  Normalizes a populations fitness
  '''
  sum_of_squares = sum(fitness**2 for fitness in fitnesses)
  if sum_of_squares == 0: return [1.0] * len(fitnesses)
  return [fitness**2 / sum_of_squares for fitness in fitnesses]


def cs461weight_constraint_fitness_func(data, max_weight):
  '''
  Evaluates a single chromosome
  '''
  def evaluate(chromosome):
    fitness, weight = 0, 0
    for idx in chromosome:
      fitness += data[idx][0]
      weight += data[idx][1]
    return fitness if weight <= max_weight else 1

  return evaluate

def abs_path(extension):
  '''Absolute file path'''
  return path.join(path.dirname(path.abspath(__file__)), extension)

def read_data(data_path):
  data = list()
  for file in glob(path.join(data_path, '*')):
    with open(path.join(data_path, file), 'r') as file:
      for line in file:
        data.append(tuple(float(i) for i in line.split()))

  return tuple(data)

def create_dir(abs_path):
  if not path.isdir(abs_path):
    mkdir(abs_path)

def logger(log_path):
  create_dir(log_path)
  avg_file = open(path.join(log_path, 'avg_fitness.txt'), 'w+')
  gen_100_file = open(path.join(log_path, 'every_100_gens.txt'), 'w+')

  def close_all():
    avg_file.close()
    gen_100_file.close()

  def log_avg(avg):
    avg_file.write(f'{avg}\n')

  def log_100_gens(maximizer, generation_num):
    gen_100_file.write(f'Generation: {generation_num}\n')
    gen_100_file.write(f'Current Population Avg fitness: {maximizer.population["avg_fitness"]}\n')
    gen_100_file.write(f'Overall Best Fitness: {maximizer.best_selection["fitness"]}\n')
    gen_100_file.write(f'Overall Best chromosome: {maximizer.best_selection["chromosome"]}\n\n')

  def save_population(chromosomes):
    with open(path.join(log_path, 'saved_population.txt'), 'w+') as f:
      f.write(str(chromosomes))
  
  return log_avg, log_100_gens, save_population, close_all



def util_over_weight(data, args):
  fitness_func = cs461weight_constraint_fitness_func(data, args.max_weight)
  x = []
  c = 0
  for u, w in data:
    x.append((c, u/w))
    c += 1

  x.sort(key=lambda x: x[1])
  print(fitness_func([d[0] for d in x[292:]]))
