'''
Ryan Phillips
nnet/utils.py

Utilities for data reading and encoding
'''
import numpy as np
import pandas as pd

def one_hot_encode(data_frame):
  '''One Hot Encodes all columns in the data frame'''
  for column in data_frame.columns:
    one_hot = pd.get_dummies(data_frame[column])
    data_frame = pd.concat([data_frame, one_hot], axis=1)
    data_frame = data_frame.drop(column, axis=1)
  return data_frame.to_numpy().astype(np.float32)

def train_test_val_splice(features, scores):
  '''Train 70/100, test 15/100, val 15/100'''
  assert features.shape[0] == scores.shape[0]
  data_len = features.shape[0]
  train_split = np.random.choice(data_len, size=int(data_len * 0.7), replace=False)
  train_x, train_y = features[train_split], scores[train_split]

  mask = np.array([True] * data_len)
  mask[train_split] = False
  unused_idxs = np.array(range(data_len))[mask]

  test_split = unused_idxs[unused_idxs.shape[0] // 2:]
  val_split = unused_idxs[:unused_idxs.shape[0] // 2]
  test_x, test_y = features[test_split], scores[test_split]
  val_x, val_y = features[val_split], scores[val_split]
  
  return (train_x, train_y), (test_x, test_y), (val_x, val_y)


def read_data_for_eval(file_name):
  data = pd.read_csv(file_name)
  scores = np.vstack([
    data.pop('math score'),
    data.pop('reading score'), 
    data.pop('writing score')]).astype(np.float32).T
  features = one_hot_encode(data)
  return features, scores

def read_encode_split_data(file_name):
  '''
  Splits annd One Hot Encodes Student Data
  '''
  data = pd.read_csv(file_name)
  scores = np.vstack([
    data.pop('math score'),
    data.pop('reading score'), 
    data.pop('writing score')]).astype(np.float32).T
  features = one_hot_encode(data)
  train, test, val = train_test_val_splice(features, scores)
  return train, test, val
