from datetime import date, datetime

import pandas as pd

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [2., 3., 4.],
    'c': ['string1', 'string2', 'string3'],
    'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
    'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
})

#%%
def write_to_excel(df, path):
    """
    pip install xlsxwriter for writing
    https://xlsxwriter.readthedocs.io/contents.html
    """


    # Exporting pandas dataframe to xlsx file
    df.to_excel(path, engine='xlsxwriter')
write_to_excel(df, ".data.xlsx")

#%%
def to_markdown(df):
    """
    pip install -U tabulate
    show markdown
    """
    print(df.to_markdown())
to_markdown(df)