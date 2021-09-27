'''
Ryan Phillips
genetics/utils.py
'''
from os import path, mkdir
from glob import glob

def abs_path(extension):
  '''Absoolute file path'''
  return path.join(path.dirname(path.abspath(__file__)), extension)

def read_data(data_path):
  utility_and_weights = list()
  for file in glob(path.join(data_path, '*')):
    with open(path.join(data_path, file), 'r') as file:
      for line in file:
        split = line.split()
        utility_and_weights.append(
          (float(split[0]), float(split[1])))
  return tuple(utility_and_weights)

def create_dir(path):
  if not path.isdir(path):
    mkdir(path)

def write_logs(log_path, avg_fitnesses):
  pass
