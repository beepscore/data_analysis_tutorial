#!/usr/bin/env python3

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
web_stats = {'Day':[1,2,3,4,5,6],
             'Visitors':[43,34,65,56,29,76],
             'Bounce_Rate':[65,67,78,65,45,52]}

df = pd.DataFrame(web_stats)

# set_index returns a new data frame
# can assign df to it using df = or using inplace
# df.set_index('Day', inplace=True)
df = df.set_index('Day')

# print(df.head)
# show last 2 rows
# print(df.tail(2))

# dataframe select a column, similar to dictionary
# print(df['Bounce_Rate'])
# shorthand, select a column similar to an attribute
# print(df.Visitors)
print(df.Visitors.tolist())

# make a data frame from a list of columns
print(df[['Visitors', 'Bounce_Rate']])

# create numpy array from pandas data frame
# this loses column headings that were in data frame
visit_bounce_array = np.array(df[['Visitors', 'Bounce_Rate']])
# print(visit_bounce_array)

# create pandas data frame from numpy array
df2 = pd.DataFrame(visit_bounce_array)
# print(df2)

houses = quandl.get('FMAC/HPI_AK')
print(houses.head)

# us_states_list is a list of dataframes
us_states_list = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states', flavor='html5lib')
print(us_states_list)
print(us_states_list[0])

# first dataframe
us_states_df = us_states_list[0]

# column 1 to end (omit column 0)
us_states = us_states_df[1:]
print(us_states)
