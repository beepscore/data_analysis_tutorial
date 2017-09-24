#!/usr/bin/env python3

# Pandas Basics - p.2 Data Analysis with Python and Pandas Tutorial
# https://pythonprogramming.net/basics-data-analysis-python-pandas-tutorial/
# https://youtu.be/0UA49Ds1XXo

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import quandl

style.use('ggplot')

# For security keep quandl api key out of version control.
# read api key from a file that is ignored.
# input_directory = "../data/input/"
# input_file_name = 'quandl_api_key.txt'
# input_file_path = input_directory + input_file_name
# rstrip to remove trailing \n
# quandl_api_key = open(input_file_path, 'r').read().rstrip()
# print('quandl_api_key', quandl_api_key)

# bounce rate is percent of visitors who come to web site page and leave without visiting any other pages
# industry average is roughly 66%
# https://en.wikipedia.org/wiki/Bounce_rate
# python dictionary
web_stats = {'Day':[1,2,3,4,5,6],
             'Visitors':[43,34,65,56,29,76],
             'Bounce_Rate':[65,67,78,65,45,52]}

# convert dictionary to pandas dataframe
df = pd.DataFrame(web_stats)

# set_index returns a new data frame
# can assign df to it using df = or using inplace
# df.set_index('Day', inplace=True)
df = df.set_index('Day')

# print(df.head)
# tail- print last 2 rows
# print(df.tail(2))

# dataframe select a column, similar to dictionary
# print(df['Bounce_Rate'])
# shorthand, select a column similar to an attribute
# print(df.Visitors)
print(df.Visitors.tolist())
# output
# [43, 34, 65, 56, 29, 76]

# note must manually close plot to enable script to continue
# df['Visitors'] or df.Visitors
# df.Visitors.plot()
# plt.show()

# make a data frame from a list of columns
print(df[['Visitors', 'Bounce_Rate']])
# output
#      Visitors  Bounce_Rate
# Day
# 1          43           65
# 2          34           67
# 3          65           78
# 4          56           65
# 5          29           45
# 6          76           52

# create numpy array from pandas data frame
# this loses column headings that were in data frame
visit_bounce_array = np.array(df[['Visitors', 'Bounce_Rate']])
# print(visit_bounce_array)

# create pandas data frame from numpy array
df2 = pd.DataFrame(visit_bounce_array)
# print(df2)

houses = quandl.get('FMAC/HPI_AK')
# print(houses.head)

# https://pythonprogramming.net/dataset-data-analysis-python-pandas-tutorial
# us_states_list is a list of dataframes
us_states_list = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states', flavor='html5lib')
# print(us_states_list)
# print(us_states_list[0])

# first dataframe
us_states_df = us_states_list[0]

# column 1 to end (omit column 0)
# us_states = us_states_df[1:]
# for abbv in us_states[1:]:

for abbv in us_states_list[0][0][1:]:
    print("FMAC/HPI_" + str(abbv))

# output
# FMAC/HPI_AL
# FMAC/HPI_AK
# FMAC/HPI_AZ
# ...
# FMAC/HPI_WY
