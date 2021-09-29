'''
Ryan Phillips

knapsack_genetic/main.py

Script that runs the genetic algorithm
'''
from argparse import ArgumentParser

from utils import abs_path, read_data, write_logs
from evolution import evolve

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
parser.add_argument('--improvement_required', type=float, default=1e-1)
parser.add_argument('--improvement_leniency', type=int, default=10)
'''
input and log path configuration
'''
parser.add_argument('--data_path', type=str, default=abs_path('./data/custom/') if not TESTING else abs_path('./data/testing'))
parser.add_argument('--log_path', type=str, default=abs_path('./logs/'))
args = parser.parse_args()

data = read_data(args.data_path)
avg_fitnesses = evolve(data, args, TESTING)
write_logs(args.log_path,avg_fitnesses)