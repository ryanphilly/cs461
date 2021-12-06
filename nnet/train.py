'''
Ryan Phillips
nnet/train.py

Script to train the network
'''
from argparse import ArgumentParser
from random import seed

from tensorflow.keras.callbacks import ModelCheckpoint

from utils import read_encode_split_data
from model import ScoreRegressor

def train(args):
  seed(43) # replicate train test split used on best model
  train, test, val = read_encode_split_data(args.data_path)
  model = ScoreRegressor([64, 128, 256], 3)
  checkpoint_callback = ModelCheckpoint(
    './ckpts/ScoreRegressor.ckpt', monitor='val_loss', verbose=0, save_best_only=True,
    save_weights_only=True, mode='auto')
   
  model.compile(optimizer='adam', loss='mse', metrics=['mae', 'acc'])
  model.fit(
    callbacks=[checkpoint_callback],
    verbose=2,
    epochs=2000,
    x=train[0], y=train[1],
    batch_size=16,
    validation_data=(val[0], val[1]))

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--data_path', type=str, default='./data/StudentsPerformance.csv')
  train(parser.parse_args())


