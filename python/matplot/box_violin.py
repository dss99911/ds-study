import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#%% box
# 백분위를 표시하는 방식

# 50% 중위값과 25%~ 75%(전체의 절반)을 box로 표시
# 특잇값을 제외한 값을 선으로 표시, 특잇값은 원으로 표시
df_state = pd.read_csv("data/state.csv")

ax = (df_state['Population']/1_000_000).plot.box(figsize=(3, 4))
ax.set_ylabel('Population (millions)')

plt.tight_layout()
plt.show()

#%% boxplot
# groupby한 box
airline_stats = pd.read_csv("data/airline_stats.csv")
airline_stats.head()
ax = airline_stats.boxplot(by='airline', column='pct_carrier_delay',
                           figsize=(5, 5))
ax.set_xlabel('')
ax.set_ylabel('Daily % of Delayed Flights')
plt.suptitle('')

plt.tight_layout()
plt.show()

#%% violinplot
# box의 한계점을 보완하여,백분위를 바이올린 처럼 표현
# inner="quartile" 사분위수를 점선으로 표현, "box" 위의 박스 처럼, 표현.

fig, ax = plt.subplots(figsize=(5, 5))
sns.violinplot(data=airline_stats, x='airline', y='pct_carrier_delay',
               ax=ax, inner='quartile', color='white')
ax.set_xlabel('')
ax.set_ylabel('Daily % of Delayed Flights')

plt.tight_layout()
plt.show()
