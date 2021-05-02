from datetime import date, datetime

import numpy as np
import pandas as pd

#%% Series

series_create_list = pd.Series([1, 3, 5, np.nan, 6, 8])
series_create_list_with_column = pd.Series({'a': 1, 'b': 5, 'c': 2, 'd': 3})
#%% Dataframe

# key : column, value : row
df_create_dataframe_by_dict = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})
df_create_dataframe_by_dict2 = pd.DataFrame(
    {
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    }
)

date_time_index = pd.date_range("20130101", periods=6)
np_dataframe_random = np.random.randn(6, 4) # 6rows, 4 columns
df_create_dataframe_index_column = pd.DataFrame(np_dataframe_random, index=date_time_index, columns=list("ABCD"))


data = [['tom', 10], ['nick', 15], ['juli', 14]]
df_create_dataframe_by_rows = pd.DataFrame(data)
df_create_dataframe_by_rows_with_column_name = pd.DataFrame(data, columns = ['Name', 'Age'])
