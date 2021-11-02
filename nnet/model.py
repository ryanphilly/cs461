import torch 
import torch.nn as nn

def weights_init_normal(module):
  if isinstance(module, (nn.Linear, nn.Conv2d)):
    module.weight.data.normal_(0.0, 1.0)
    if module.bias.data is not None:
      module.bias.data.zero_()

def linear_block(in_channels, out_channels, non_linearity='relu', batch_norm=True, dropout=False):
  modules = [nn.Linear(in_channels, out_channels, bias=True)]
  if batch_norm:
    modules.append(nn.BatchNorm1d(out_channels))
  if non_linearity == 'relu':
    modules.append(nn.ReLU(inplace=True))
  elif non_linearity == 'tanh':
    modules.append(nn.Tanh())
  if dropout:
    modules.append(nn.Dropout())

  return nn.Sequential(*modules)

class NonLinearRegressor(nn.Module):
  def __init__(self, feature_dims=[5, 64, 128], num_predictions=3):
    assert len(feature_dims) >= 2
    assert isinstance(num_predictions, int)
    super(NonLinearRegressor, self).__init__()

    self.hidden_layers = nn.Sequential(*[
      linear_block(feature_dims[c], feature_dims[c+1])
        for c in range(len(feature_dims) - 1)
    ])
    self.predictions = nn.Linear(feature_dims[-1], num_predictions)
  
  def forward(self, x):
    return self.predictions(self.hidden_layers(x))