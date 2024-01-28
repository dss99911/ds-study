# %% set virtual environment
# https://yarn.dask.org/en/stable/environments.html
# if set local env tar.gz file. it uploads to hdfs whenever run the application.
# for preventing upload env file. upload to hdfs. and set the hdfs file path
from dask.distributed import Client
from dask_yarn import YarnCluster

cluster = YarnCluster(environment='my-env.tar.gz')
# cluster = YarnCluster() # you can set the path on ~/.config/dask/yarn.yaml
client = Client(cluster)
print(client.get_versions(check=True))
# version
# {'scheduler': {'host': {'python': '3.7.16.final.0', 'python-bits': 64, 'OS': 'Linux',
#                         'OS-release': '4.14.313-235.533.amzn2.x86_64', 'machine': 'x86_64', 'processor': 'x86_64',
#                         'byteorder': 'little', 'LC_ALL': 'None', 'LANG': 'en_US.UTF-8'},
#                'packages': {'python': '3.7.16.final.0', 'dask': '2022.02.0', 'distributed': '2022.02.0',
#                             'msgpack': '1.0.5', 'cloudpickle': '2.2.1', 'tornado': '6.2', 'toolz': '0.12.0',
#                             'numpy': '1.21.6', 'pandas': '1.3.5', 'lz4': None, 'blosc': None}}, 'workers': {},
#  'client': {'host': {'python': '3.7.16.final.0', 'python-bits': 64, 'OS': 'Linux',
#                      'OS-release': '4.14.313-235.533.amzn2.x86_64', 'machine': 'x86_64', 'processor': 'x86_64',
#                      'byteorder': 'little', 'LC_ALL': 'None', 'LANG': 'en_US.UTF-8'},
#             'packages': {'python': '3.7.16.final.0', 'dask': '2022.02.0', 'distributed': '2022.02.0',
#                          'msgpack': '1.0.5', 'cloudpickle': '2.2.1', 'tornado': '6.2', 'toolz': '0.12.0',
#                          'numpy': '1.21.6', 'pandas': '1.3.5', 'lz4': None, 'blosc': None}}}

#%%

# https://yarn.dask.org/en/latest/
# pip install dask-yarn
from dask_yarn import YarnCluster
from dask.distributed import Client

# Create a cluster where each worker has two cores and eight GiB of memory
cluster = YarnCluster(environment='environment.tar.gz',
                      worker_vcores=2,
                      worker_memory="8GiB")
# Scale out to ten such workers
cluster.scale(10)

# Adaptively scale between 2 and 10 workers
cluster.adapt(minimum=2, maximum=10)

# Connect to the cluster
client = Client(cluster)

#%% shoutdown
# Use ``YarnCluster`` as a context manager
with YarnCluster() as cluster:
    pass
    # The cluster will remain active inside this block,
    # and will be shutdown when the context exits.

# Or manually call `shutdown`
cluster = YarnCluster()
# ...
cluster.shutdown()

#%% install libraries on task node
# https://yarn.dask.org/en/latest/environments.html
from dask_yarn import YarnCluster
from dask.distributed import Client

# by archiving
cluster = YarnCluster(environment='my-env.tar.gz')
client = Client(cluster)
client.get_versions(check=True)  # check that versions match between all nodes

from dask_yarn import YarnCluster

# Use a conda environment at /path/to/my/conda/env
cluster = YarnCluster(environment='conda:///path/to/my/conda/env')
# Use a virtual environment at /path/to/my/virtual/env
cluster = YarnCluster(environment='venv:///path/to/my/virtual/env')
# Use a Python executable at /path/to/my/python
cluster = YarnCluster(environment='python:///path/to/my/python')


#%% submit by dask-yarn.
# it uses the yarn cluster which is already created on the cluster.
# if use YarnCluster(...), it means it create the yarn cluster
# https://yarn.dask.org/en/latest/submit.html
cluster = YarnCluster.from_current()  #use this instead of cluster = YarnCluster(...)
# dask-yarn submit \
#   --environment my_env.tar.gz \
#   --worker-count 8 \
#   --worker-vcores 2 \
#   --worker-memory 4GiB \
#   myscript.py