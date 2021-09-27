'''
Ryan Phillips

knapsack_genetic/standard/operations.py
'''
from random import sample, randint, random

def generate_init_population(data, data_idxs, pop_size, num_samples, max_weight):
  '''
  Generates a population with random selections

  "data" utils and weights
  "data_idxs" range(len(utils and weights))\n
  "pop_size" size of population to generate\n
  "num_samples" how many items should be in each selection
  "max_weight" knapsack weight limit

  return:
    population list[set{indexes of selected items}]\n
    fitnesses list[float]\n
    avg_fitness: float\n
    sum_of_squares: float\n
  '''
  population, fitnesses = list(), list()
  sum_of_sqaures, total_fitness = 0, 0
  for idx in range(pop_size):
    selection = set(sample(data_idxs, num_samples))
    fitness = evaluate_selection(data, selection, max_weight)
    sum_of_sqaures += fitness**2
    total_fitness += fitness
    population.append(selection)
    fitnesses.append((idx, fitness))
  return population, fitnesses, total_fitness / pop_size, sum_of_sqaures

def random_bitflip_mutation(item_idx, selection, mutation_rate):
  '''
  mutation_rate chance of bitflip for current index
  '''
  if random() <= mutation_rate:
    selection.remove(item_idx) if item_idx in selection else selection.add(item_idx)

def sp_crossover(data_idxs, mom_genes, dad_genes, mutation_rate):
  '''
  Performs Single Point Crossover w/ stochastic biitflip mutation

  "data_idxs" range(len(utils and weights))\n
  "mom_genes" indexes of selected items in moms genes\n
  "dad_genes" indexes of selected items in dads genes\n
  "mutation_rate" probability of bitflip per item

  return: (son_genes, daughter_genes) - indexes of offspring
  '''
  # at least one gene from mom and dad
  divider = randint(1, len(data_idxs)-2)

  son_genes, daughter_genes = set(), set()
  for idx in data_idxs:
    # single point crossover
    if idx in mom_genes:
      if idx < divider:
        son_genes.add(idx)
      else:
        daughter_genes.add(idx)
    if idx in dad_genes:
      if idx < divider:
        daughter_genes.add(idx)
      else:
        son_genes.add(idx)

    # bitflip mutations
    random_bitflip_mutation(idx, son_genes, mutation_rate)
    random_bitflip_mutation(idx, daughter_genes, mutation_rate)

  return son_genes, daughter_genes

def evaluate_selection(data, selection, max_weight):
  '''
  Evaluates a single selection
  '''
  fitness, weight = 0, 0
  for idx in selection:
    fitness += data[idx][0]
    weight += data[idx][1]
  return fitness if weight <= max_weight else 1

def l2norm(population_fitnesses, sum_of_squares=0):
  '''
  Normalizes a populations fitness
  '''
  if sum_of_squares == 0:
    sum_of_squares = sum(fitness**2 for fitness in population_fitnesses)
  assert sum_of_squares != 0

  normalized = list()
  for fitness in population_fitnesses:
    normalized.append((fitness[0], fitness[1]**2 / sum_of_squares))
  return normalized


if __name__ == '__main__':
  from utils import abs_path, read_data
  from time import perf_counter
