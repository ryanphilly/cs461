import torch
import numpy as np
import pandas as pd

from model import NonLinearRegressor


def read_and_prepare_data(file_name='./data/StudentsPerformance.csv'):
  data = pd.read_csv(file_name)

  scores = torch.from_numpy(np.vstack([
    data.pop('math score'),
    data.pop('reading score'), 
    data.pop('writing score')]).astype(np.float32)).T

  for column in data.columns:
    categories = { category: value
      for value, category in enumerate(data[column].unique())}
    data[column] = data[column].map(categories)

  features = torch.from_numpy(data.to_numpy().astype(np.float32))

  return features, scores

def train():
  features, scores = read_and_prepare_data()
  model = NonLinearRegressor(feature_dims=[5, 64, 128])
  optimizer = torch.optim.Adam(model.parameters())
  criterion = torch.nn.MSELoss()
  model.train()
  for _ in range(10000):
    total_loss = 0
    for batch in range(0, 1000, 128):
      model.zero_grad()
      preds = model(features[batch:batch+128])
      loss = criterion(preds, scores[batch: batch+128])
      total_loss += loss.item()
      loss.backward()
      optimizer.step()
    
    model.eval()
    print(total_loss / (1000 / 128))
    print(model(features[0:5]), scores[0:5])
    model.train()

train()