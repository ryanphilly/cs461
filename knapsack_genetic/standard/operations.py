'''
Ryan Phillips

knapsack_genetic/standard/operations.py
'''
from random import (
  sample, randint, random, choices)

from standard.population import Population

def generate_init_population(data, data_idxs, pop_size, num_samples, max_weight):
  '''
  Generates a population with random chromosomes

  "data" utils and weights
  "data_idxs" range(len(utils and weights))\n
  "pop_size" size of population to generate\n
  "num_samples" how many items should be in each chromosome
  "max_weight" knapsack weight limit

  return:
    population: Population
    sum_of_squares: float\n
  '''
  chromosomes, fitnesses = list(), list()
  sum_of_sqaures, total_fitness = 0, 0
  for _ in range(pop_size):
    chromosome = set(sample(data_idxs, num_samples))
    fitness = evaluate_chromosome(data, chromosome, max_weight)
    chromosomes.append(chromosome)
    fitnesses.append(fitness)

    sum_of_sqaures += fitness**2
    total_fitness += fitness

  population = Population(chromosomes, fitnesses,
    avg_fitness=total_fitness / pop_size)
  return population, sum_of_sqaures

def random_bitflip_mutation(item_idx, chromosome, mutation_rate):
  '''
  mutation_rate chance of bitflip for current index
  '''
  if random() <= mutation_rate:
    chromosome.remove(item_idx) if item_idx in chromosome else chromosome.add(item_idx)

def sp_crossover(data_idxs, mom_chromosome, dad_chromosome, mutation_rate):
  '''
  Performs Single Point Crossover w/ stochastic biitflip mutation

  "data_idxs" range(len(utils and weights))\n
  "mom_chromosome" indexes of selected items in parent 1\n
  "dad_chromosome" indexes of selected items in parent 2\n
  "mutation_rate" probability of bitflip per item

  return: (son_chromosome, daughter_chromosome) - indexes of offspring
  '''
  # at least one gene from mom and dad
  divider = randint(1, len(data_idxs)-2)
  son_chromosome, daughter_chromosome = set(), set()
  for idx in data_idxs:
    # single point crossover
    if idx in mom_chromosome:
      if idx < divider:
        son_chromosome.add(idx)
      else:
        daughter_chromosome.add(idx)
    if idx in dad_chromosome:
      if idx < divider:
        daughter_chromosome.add(idx)
      else:
        son_chromosome.add(idx)

    # bitflip mutations
    random_bitflip_mutation(idx, son_chromosome, mutation_rate)
    random_bitflip_mutation(idx, daughter_chromosome, mutation_rate)

  return son_chromosome, daughter_chromosome


def breed_next_generation(data, data_idxs,
                          population,
                          max_weight,
                          mutation_rate,
                          normal_fitnesses=None,
                          deallocate_ancestors=True):
  '''
  Perfroms fitness proportionate selection
  and breeds a new generation of chronosomes
  '''
  if normal_fitnesses is None:
    normal_fitnesses = l2norm(population.fitnesses)

  # still need to cull

  pop_size = len(population.chromosomes)
  breeding_pool = choices(population.chromosomes, weights=normal_fitnesses, k=pop_size)

  new_chromosomes, new_fitnesses = list(), list()
  sum_of_squares, total_fitness = 0, 0

  for idx in range(pop_size // 2):
    son, daughter = sp_crossover(
      data_idxs,
      breeding_pool[idx],
      breeding_pool[pop_size-idx-1],
      mutation_rate)
    son_fitness = evaluate_chromosome(data, son, max_weight)
    daughter_fitness = evaluate_chromosome(data, daughter, max_weight)

    new_chromosomes.extend([son, daughter])
    new_fitnesses.extend([son_fitness, daughter_fitness])

    sum_of_squares += son_fitness**2 + daughter_fitness**2
    total_fitness += son_fitness + daughter_fitness

  if deallocate_ancestors:
    population.deallocate_for_logging()

  new_population = Population(new_chromosomes, new_fitnesses, total_fitness / pop_size)
  return new_population, sum_of_squares


def evaluate_chromosome(data, chromosome, max_weight):
  '''
  Evaluates a single chromosome
  '''
  fitness, weight = 0, 0
  for idx in chromosome:
    fitness += data[idx][0]
    weight += data[idx][1]
  return fitness if weight <= max_weight else 1

def l2norm(population_fitnesses, sum_of_squares=0):
  '''
  Normalizes a populations fitness
  '''
  if sum_of_squares == 0:
    sum_of_squares = sum(fitness**2 for fitness in population_fitnesses)
  return [fitness**2 / sum_of_squares for fitness in population_fitnesses]