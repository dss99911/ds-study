# Init
from datetime import date, datetime

import sqlite3
import pandas as pd

con = sqlite3.connect("database.sqlite")
df = pd.read_sql_query("SELECT * from existing_table", con)
df.to_sql("new_table", con, if_exists="replace")
con.close()

# %%
