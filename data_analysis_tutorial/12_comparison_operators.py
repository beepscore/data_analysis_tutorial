#!/usr/bin/env python3

# Tutorial 7 Pickling
# https://pythonprogramming.net/pickle-data-analysis-python-pandas-tutorial/

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

# Tutorial 12 Applying Comparison Operators to DataFrame
# https://pythonprogramming.net/comparison-operators-data-analysis-python-pandas-tutorial/

# note 6212 must be an erroneous reading, bridge can't be that height
# may indicate sensor interference or problem
bridge_height = {'meters': [10.26, 10.31, 10.27, 10.22, 10.23, 6212.42, 10.28, 10.25, 10.31]}

df = pd.DataFrame(bridge_height)
df['STD'] = df['meters'].rolling(window=2, center=False).std()
print(df)

# std for entire series
df_meters_describe = df.describe()['meters']
print()
print(df_meters_describe)
df_meters_std = df_meters_describe['std']
# df.plot()
# plt.show()

# filter with a comparison operator. Don't pass outliers
df = df[(df['STD'] < 1.5 * df_meters_std)]

df['meters'].plot()
plt.show()
