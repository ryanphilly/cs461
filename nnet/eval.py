from argparse import ArgumentParser

import tensorflow as tf

from utils import read_data_for_eval
from model import ScoreRegressor

def eval(args):
  features, _ = read_data_for_eval(args.data_path)
  latest = tf.train.latest_checkpoint('./ckpts')
  model = ScoreRegressor([64, 128, 256], 3)
  model.load_weights(latest).expect_partial()
  preds = model.predict(features, batch_size=64)
  print(preds)

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--data_path', type=str, default='./data/StudentsPerformance.csv')
  eval(parser.parse_args())