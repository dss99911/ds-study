from datetime import date, datetime

import numpy as np
import pandas as pd
from pandas import DataFrame
#%% parquet


df_from_parquet = pd.read_parquet("path")

#%% csv
df_from_csv = pd.read_csv("path")

#%% excel
df_from_excel: DataFrame = pd.read_excel("path", index_col=0)
