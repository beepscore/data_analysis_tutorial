#!/usr/bin/env python3

import pandas as pd

# tutorial 6 Concatenating and appending dataframes
# https://pythonprogramming.net/join-merge-data-analysis-python-pandas-tutorial/

# copy initial dataframes from tutorial web page, edit per PEP8

df1 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Int_rate': [2, 3, 2, 2],
                    'US_GDP_Thousands': [50, 55, 65, 55]},
                   index=[2001, 2002, 2003, 2004])

df2 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Int_rate': [2, 3, 2, 2],
                    'US_GDP_Thousands': [50, 55, 65, 55]},
                   index=[2005, 2006, 2007, 2008])

# Unemployment column is different from tutorial 5
df3 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Unemployment': [7, 8, 9, 6],
                    'Low_tier_HPI': [50, 52, 50, 53]},
                   index=[2001, 2002, 2003, 2004])

# merge - in this case merge is not ideal. It ignores index, duplicates some rows.
# merge is most useful when importing database tables with a common key e.g. username
d1_d3 = pd.merge(df1, df3, on='HPI')
print()
print('merge df1 df3. Note duplicate rows e.g. in unemployment')
print(d1_d3)

# merge multiple columns. this eliminates some duplication, but not all
d1_d2 = pd.merge(df1, df2, on=['HPI', 'Int_rate'])
print()
print('merge df1 df2')
print(d1_d2)

# prepare for join. after set_index, df1 and df3 share an index but don't share any columns
df1.set_index('HPI', inplace=True)
df3.set_index('HPI', inplace=True)

# join - 'honors' index
# j_d1_d3 = df1.join(df3, lsuffix='_df1', rsuffix='_df3')
j_d1_d3 = df1.join(df3)
print()
print('join')
print(j_d1_d3)


# similar to above, remove indexes and HPI, add Year
df1 = pd.DataFrame({'Year': [2001, 2002, 2003, 2004],
                    'Int_rate': [2, 3, 2, 2],
                    'US_GDP_Thousands': [50, 55, 65, 55]})

# skip 2002
df3 = pd.DataFrame({'Year': [2001, 2003, 2004, 2005],
                    'Unemployment': [7, 8, 9, 6],
                    'Low_tier_HPI': [50, 52, 50, 53]})

# left joins on left dataframe (here df1)
# right joins on right dataframe (here df3)
# inner joins on keys intersection - default
# outer joins on keys union
merged = pd.merge(df1, df3, on='Year', how='outer')
merged.set_index('Year', inplace=True)
print()
print(merged)
