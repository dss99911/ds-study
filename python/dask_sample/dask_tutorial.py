import numpy as np
import pandas as pd

import dask.dataframe as dd
import dask.array as da
import dask.bag as db

#%% create dataframe
index = pd.date_range("2021-09-01", periods=2400, freq="1H")
df = pd.DataFrame({"a": np.arange(2400), "b": list("abcaddbe" * 300)}, index=index)
ddf = dd.from_pandas(df, npartitions=10)  # set partition
ddf

partition = ddf.partitions[1]  # get a partition

not_yet_computed = ddf["2021-10-01": "2021-10-09 5:00"]
not_yet_computed.compute()

#%% Series
ddf.b
ddf.a.mean().compute()
#%% create array
import numpy as np
import dask.array as da

data = np.arange(100_000).reshape(200, 500)
a = da.from_array(data, chunks=(100, 100))
a

# inspect the chunks
a.chunks
# access a particular block of data
a.blocks[1, 3]

a[:50, 200]
a.T.compute()
#%% create bag
b = db.from_sequence([1, 2, 3, 4, 5, 6, 2, 1], npartitions=2)
b.filter(lambda x: x % 2)
b.distinct()
c = db.zip(b, b.map(lambda x: x * 10))

#%% graph
result = ddf["2021-10-01": "2021-10-09 5:00"].a.cumsum() - 100
result.dask
result.visualize()

