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
  data = list()
  for file in glob(path.join(data_path, '*')):
    with open(path.join(data_path, file), 'r') as file:
      for line in file:
        data.append(tuple(float(i) for i in line.split()))

  return tuple(data)

def create_dir(path):
  if not path.isdir(path):
    mkdir(path)

def write_logs(log_path, avg_fitnesses):
  pass
