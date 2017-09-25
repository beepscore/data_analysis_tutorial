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

df3 = pd.DataFrame({'HPI': [80, 85, 88, 85],
                    'Unemployment': [7, 8, 9, 6],
                    'Low_tier_HPI': [50, 52, 50, 53]},
                   index=[2001, 2002, 2003, 2004])

# merge
d1_d3 = pd.merge(df1, df3, on='HPI')
print(d1_d3)

# this creates many NaN elements, join/merge may work better
print()

# join
