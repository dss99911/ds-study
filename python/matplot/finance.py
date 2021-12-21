# https://pypi.org/project/mplfinance/
# https://github.com/matplotlib/mplfinance.git
# pip install --upgrade mplfinance
# %%
import mplfinance as mpf

import pandas as pd

daily = pd.read_csv('data/SP500_NOV2019_Hist.csv', index_col=0, parse_dates=True)
daily.index.name = 'Date'
mpf.plot(daily, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=True)