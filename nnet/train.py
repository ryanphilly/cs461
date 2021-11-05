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
  model = NonLinearRegressor(feature_dims=[5, 128])
  optimizer = torch.optim.Adam(model.parameters())
  criterion = torch.nn.MSELoss()
  model.train()

  for epoch in range(100000):
    for batch in range(64, 1000, 64):
      model.zero_grad()
      preds = model(features[batch:batch+64])
      loss = criterion(preds, scores[batch: batch+64])
      loss.backward()
      optimizer.step()

    if epoch % 100 == 0:
      model.eval()
      with torch.no_grad():
        v_preds = model(features[0:64])
        accuracy = torch.mean(
          torch.abs(v_preds - scores[0:64]), dim=0)
        print(accuracy)
      model.train()

train()