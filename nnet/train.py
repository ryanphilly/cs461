'''
Ryan Phillips
nnet/train.py

Script to train the network
'''
from argparse import ArgumentParser

from utils import read_and_encode_data
from model import ScoreRegressor

def train():
  features, scores = read_and_encode_data('./data/StudentsPerformance.csv')
  model = ScoreRegressor([64, 128, 256, 512, 512], 3)
  model.compile(optimizer='adam', loss='mse', metrics=['mae', 'acc'])
  for epoch in range(10000):
    model.fit(x=features, y=scores, batch_size=64)

if __name__ == '__main__':
  parser = ArgumentParser() # TODO
  train()


