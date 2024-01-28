#%% Scheduling
from dask.distributed import Client


client = Client()  # use local only
client = Client("<url-of-scheduler>")  # connect to remote cluster

# Diagnostics for distributed cluster
# port is different by application.
client.dashboard_link  # 'http://127.0.0.1:8787/status'
