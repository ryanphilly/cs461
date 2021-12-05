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

def read_and_encode_data(file_name):
  '''
  One Hot Encodes Student Data
  '''
  data = pd.read_csv(file_name)
  scores = np.vstack([
    data.pop('math score'),
    data.pop('reading score'), 
    data.pop('writing score')]).astype(np.float32).T
  features = one_hot_encode(data)
  return features, scores