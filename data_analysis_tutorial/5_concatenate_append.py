#!/usr/bin/env python3

import pandas as pd

# tutorial 5 Concatenating and appending dataframes
# https://pythonprogramming.net/concatenate-append-data-analysis-python-pandas-tutorial/

# copy initial dataframes from tutorial web page, edit per PEP8

df1 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Int_rate': [2, 3, 2, 2],
                    'US_GDP_Thousands': [50, 55, 65, 55]},
                   index=[2001, 2002, 2003, 2004])

# similar to df1, index years are later
df2 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Int_rate': [2, 3, 2, 2],
                    'US_GDP_Thousands': [50, 55, 65, 55]},
                   index=[2005, 2006, 2007, 2008])

# index years same as df1, columns are different
df3 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Int_rate': [2, 3, 2, 2],
                    'Low_tier_HPI': [50, 52, 50, 53]},
                   index=[2001, 2002, 2003, 2004])

# concatenate
d1_d2 = pd.concat([df1, df2])
print(d1_d2)

# this creates many NaN elements, join/merge may work better
d1_d2_d3 = pd.concat([df1, df2, df3])
print()
print(d1_d2_d3)

# append- for these dataframes, append is similar to concatenate
# Note dataframe append is not super efficient.
# If you want to append frequently, it may be better to use a database.
# Then pull from database into pandas dataframe for analysis/plotting
df4 = df1.append(df2)
print()
print(df4)

df5 = df1.append(df3)
print()
print(df5)

# append new row, loses index
s = pd.Series([80, 2, 50], index=['HPI', 'Int_rate', 'US_GDP_Thousands'])
df6 = df1.append(s, ignore_index=True)
print()
print(df6)
