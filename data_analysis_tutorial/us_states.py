#!/usr/bin/env python3

# Building dataset - p.4 Data Analysis with Python and Pandas Tutorial
# https://pythonprogramming.net/dataset-data-analysis-python-pandas-tutorial/

# https://youtu.be/9Z7wvippeko

import pandas as pd
from matplotlib import style
import quandl

style.use('ggplot')

# anonymous request, doesn't require authtoken
# comment out to avoid quandl.errors.quandl_error.LimitExceededError: (Status 429)
# You have exceeded the anonymous user limit of 50 calls per day.
# To make more calls today, please register for a free Quandl account and then include your API key with your requests.
# houses = quandl.get('FMAC/HPI_AK')

# authtoken
# For security keep quandl api key out of version control.
# read api key from a file that is ignored.
# input_directory = "../data/input/"
# input_file_name = 'quandl_api_key.txt'
# input_file_path = input_directory + input_file_name
# rstrip to remove trailing \n
# quandl_api_key = open(input_file_path, 'r').read().rstrip()
# print('quandl_api_key', quandl_api_key)

# request with authtoken
# houses = quandl.get('FMAC/HPI_AK', authtoken=quandl_api_key)

# print(houses.head())

# https://pythonprogramming.net/dataset-data-analysis-python-pandas-tutorial
# us_states_list is a list of dataframes
us_states_list = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states', flavor='html5lib')

# first dataframe
us_states_df = us_states_list[0]

abbreviation_series = us_states_df[0]
# note series contains index and value, loop uses value
# print('abbreviation_series')
# print(abbreviation_series)

# row 1 to end (omit row0, contains series name 'Abbreviation')
abbreviations = abbreviation_series[1:]
# print('abbreviations')
# print(abbreviations)

for abbreviation in abbreviations:
    print("FMAC/HPI_" + str(abbreviation))

# output
# FMAC/HPI_AL
# FMAC/HPI_AK
# FMAC/HPI_AZ
# ...
# FMAC/HPI_WY
