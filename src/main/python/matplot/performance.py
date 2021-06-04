#%%
# https://matplotlib.org/stable/tutorials/introductory/usage.html#performance

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# Setup, and create the data to plot
y = np.random.rand(100000)
y[50000:] *= 2
y[np.geomspace(10, 50000, 400).astype(int)] = -1
mpl.rcParams['path.simplify'] = True

# no simplifying
mpl.rcParams['path.simplify_threshold'] = 0.0
plt.plot(y)
plt.show()

# simplifying
mpl.rcParams['path.simplify_threshold'] = 1.0
plt.plot(y, markevery=10)
plt.show()

#%%
# Splitting lines into smaller chunks
# https://matplotlib.org/stable/tutorials/introductory/usage.html#splitting-lines-into-smaller-chunks
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['path.simplify_threshold'] = 1.0

# Setup, and create the data to plot
y = np.random.rand(100000)
y[50000:] *= 2
y[np.geomspace(10, 50000, 400).astype(int)] = -1
mpl.rcParams['path.simplify'] = True

mpl.rcParams['agg.path.chunksize'] = 0
plt.plot(y)
plt.show()

mpl.rcParams['agg.path.chunksize'] = 10000
plt.plot(y)
plt.show()

#%%
# https://matplotlib.org/stable/tutorials/introductory/usage.html#using-the-fast-style
import matplotlib.style as mplstyle
mplstyle.use(['dark_background', 'ggplot', 'fast'])