import matplotlib.pyplot as plt
import numpy as np
import pandas

# Numpy Array만 지원하므로, Pandas Dataframe, Numpy Matrix도 array로 변환해서, 호출해야함


#%% Pandas
a = pandas.DataFrame(np.random.rand(4, 5), columns = list('abcde'))
a_asarray = a.values

#%% Numpy Matrix
b = np.matrix([[1, 2], [3, 4]])
b_asarray = np.asarray(b)