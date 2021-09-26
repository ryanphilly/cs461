'''
Ryan Phillips

knapsack_genetic/standard/evolution.py
'''

from multiprocessing import Pool, cpu_count

from operations import (
  generate_init_population,
  sp_crossover,
  evaluate_selection,
  l2norm
)

def evolve(data, args):
  pass