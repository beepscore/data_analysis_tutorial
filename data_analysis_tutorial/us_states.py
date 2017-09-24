#!/usr/bin/env python3

# IO Basics - p.3 Data Analysis with Python and Pandas Tutorial
# https://pythonprogramming.net/input-output-data-analysis-python-pandas-tutorial/
# https://youtu.be/9Z7wvippeko

import pandas as pd
from matplotlib import style
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
