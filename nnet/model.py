'''
Ryan Phillips
nnet/model.py

Multi Layer Perceptron
'''
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential


def dense_block(out_channels, activation='relu', batch_norm=True, drop_out=True):
  '''
  Single hidden layer in the network
  '''
  block = Sequential()

  if drop_out:
    block.add(Dropout(0.2)) # 20% chance for each neruon to be dropped

  block.add(Dense( # gaussian weights, mean=1, std=0.2, no bias, (Y = W.X)
    out_channels,
    activation=activation,
    use_bias=True,
    kernel_initializer=tf.random_normal_initializer(0.0, 0.2)))

  if batch_norm:
    block.add(BatchNormalization())

  return block

class ScoreRegressor(Model):
  '''Standard MLP Regressor'''
  def __init__(self, hidden_channels, out_channels):
    super(ScoreRegressor, self).__init__()

    self.mlps = Sequential()
    for i, width in enumerate(hidden_channels):
      if i == 0:
        self.mlps.add(dense_block(width, drop_out=False))
      else:
        self.mlps.add(dense_block(width))

    self.preds = dense_block(
      out_channels, activation=None, batch_norm=False, drop_out=False)

  def call(self, x):
    return self.preds(self.mlps(x))


