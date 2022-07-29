from torch import nn

nn.MSELoss  # Mean Square Error. for regression
nn.NLLLoss # Negative Log Likelihood. for classification
loss_fn = nn.CrossEntropyLoss() # for classification. combine nn.LogSoftmax and nn.NLLLoss


