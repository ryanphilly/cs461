'''
Ryan Phillips

knapsack_genetic/generator.py
'''
from random import choices, randint, random, sample

from utils import l2norm

class Generator(object):
  def __init__(self, data, fitness_func, init_pop_size, init_selection_size, mutation_rate):
    self.data_idxs = range(len(data))
    self.population = dict()
    self.best_selection = { 'fitness': 0.0, 'chromosome': set() }
    self.fitness_func = fitness_func
    self.mutation_rate = mutation_rate
    self._generate_init_population(init_pop_size, init_selection_size)

  def get_normal_fitness(self):
    return l2norm(self.population['fitnesses'])

  def step(self):
    '''
    Generates new population by applying 
    fitness proportionate selection and
    single point crossover with a random bitflip mutation
    '''
    # Fitness proportionate selection
    breeding_pool = choices(
      self.population['chromosomes'],
      k=len(self.population['chromosomes']),
      weights=self.get_normal_fitness())
      
    # single point crossover with random bitflip mutation
    new_chromosomes, new_fitnesses, total_fitness = list(), list(), 0
    for idx in range(len(breeding_pool) // 2):
      son, daughter = self._breed(
        breeding_pool[idx],
        breeding_pool[len(breeding_pool)-idx-1],
        self.mutation_rate)

      son_fitness = self.fitness_func(son)
      daughter_fitness = self.fitness_func(daughter)
      new_chromosomes.extend([son, daughter])
      new_fitnesses.extend([son_fitness, daughter_fitness])
      total_fitness += son_fitness + daughter_fitness

    self.population = {
      'chromosomes': new_chromosomes,
      'fitnesses': new_fitnesses,
      'total_fitness': total_fitness,
      'avg_fitness': total_fitness / len(breeding_pool)
    }
    self._update_best()

    return self.population

  def _generate_init_population(self, population_size, selection_size):
    '''
    Generates an initial population of random selected chromosomes
    '''
    chromosomes, fitnesses, total_fitness = list(), list(), 0
    for _ in range(population_size):
      chromosome = set(sample(self.data_idxs, selection_size))
      fitness = self.fitness_func(chromosome)
      chromosomes.append(chromosome)
      fitnesses.append(fitness)
      total_fitness += fitness

    self.population = {
      'chromosomes': chromosomes,
      'fitnesses': fitnesses,
      'total_fitness': total_fitness,
      'avg_fitness': total_fitness / population_size
    }
    self._update_best()
    
  def _breed(self, mom_chromosome, dad_chromosome, mutation_rate):
    '''
    Single Point Crossover w/ bitflip mutation

    "mom_chromosome" indexes of selected items in parent 1
    "dad_chromosome" indexes of selected items in parent 2
    "mutation_rate" P(bitflip) for all genes

    return: (son_chromosome, daughter_chromosome)
    '''
    # at least one gene from mom and dad
    divider = randint(1, len(self.data_idxs)-2)

    son_chromosome, daughter_chromosome = set(), set()
    for idx in self.data_idxs:
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

      # stochastic bitflip mutation
      if random() <= mutation_rate:
        son_chromosome.remove(idx) if idx in son_chromosome \
          else son_chromosome.add(idx)
      if random() <= mutation_rate:
        daughter_chromosome.remove(idx) if idx in daughter_chromosome \
          else daughter_chromosome.add(idx)

    return son_chromosome, daughter_chromosome
  
  def _update_best(self):
    best_idx = max(range(len(self.population['chromosomes'])), key=self.population['fitnesses'].__getitem__)
    if self.population['fitnesses'][best_idx] > self.best_selection['fitness']:
      self.best_selection = {
        'chromosome': self.population['chromosomes'][best_idx],
        'fitness': self.population['fitnesses'][best_idx]
      }

