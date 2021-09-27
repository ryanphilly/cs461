'''
Ryan Phillips

knapsack_genetic/main.py

Script that runs the genetic algorithm
'''
from argparse import ArgumentParser
from utils import abs_path, read_data, write_logs

TESTING = True

parser = ArgumentParser()

'''
knapsack configuration:
'''
parser.add_argument('--max_weight', type=float, default=5e2)

'''
genetic algorithm configuration
'''
parser.add_argument('--init_population', type=int, default=1000)
parser.add_argument('--init_num_samples', type=int, default=20)
parser.add_argument('--mutation_rate', type=float, default=1e-4)
parser.add_argument('--terminate_improvement', type=float, default=1e-1)
parser.add_argument('--terminates_needed', type=int, default=10)
'''
input and log path configuration
'''
parser.add_argument('--data_path', type=str, default=abs_path('./data/custom/') if not TESTING else abs_path('./data/testing'))
parser.add_argument('--log_path', type=str, default=abs_path('./logs/'))

'''
--vectorized=bool
default=False

Set to true if you have PyTorch installed
if a CUDA compatible GPU is detected it will be used

tested w/ pytorch 1.9.0
'''
parser.add_argument('--vectorized', type=bool, default=False)

args = parser.parse_args()
if args.vectorized:
  try:
    import torch
    import  torch.nn
  except ImportError:
    raise ImportError('PyTorch required for vectorized implementation')
  from vectorized.evolution import evolve
else:
  from standard.evolution import evolve

data = read_data(args.data_path)
if args.vectorized:
  # (1, 2, N)
  data  = torch.Tensor(data) \
    .view(-1, len(data)).unsqueeze(0)

avg_fitnesses = evolve(data, args, TESTING)
write_logs(args.log_path,avg_fitnesses)